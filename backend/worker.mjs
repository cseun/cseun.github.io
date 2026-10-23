const json = (data, status = 200) => Response.json(data, { status });
async function digest(value) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value)))].map(b => b.toString(16).padStart(2, '0')).join('');
}
async function limited(env, key, max, seconds) {
  const now = Math.floor(Date.now() / 1000);
  const row = await env.DB.prepare(`INSERT INTO limits(key,count,expires) VALUES (?,1,?) ON CONFLICT(key) DO UPDATE SET count=CASE WHEN expires<=? THEN 1 ELSE count+1 END, expires=CASE WHEN expires<=? THEN excluded.expires ELSE expires END RETURNING count`).bind(key, now + seconds, now, now).first();
  return row.count > max;
}
async function route(request, env) {
  const url = new URL(request.url), path = url.pathname;
  const now = Math.floor(Date.now() / 1000);
  if (!env.ADMIN_PASSWORD || !env.IP_SALT) return json({ error: '서버 설정을 준비 중입니다.' }, 503);
  const ip = await digest(env.IP_SALT + (request.headers.get('CF-Connecting-IP') || 'unknown'));
  if (request.method === 'GET' && path === '/comments') {
    const before = Number(url.searchParams.get('before') || Number.MAX_SAFE_INTEGER);
    if (!Number.isSafeInteger(before) || before < 1) return json({ error: '잘못된 페이지입니다.' }, 400);
    const { results } = await env.DB.prepare('SELECT id,name,message,created_at FROM comments WHERE id < ? ORDER BY id DESC LIMIT 21').bind(before).all();
    return json({ comments: results.slice(0, 20), next: results.length > 20 ? results[19].id : null });
  }
  if (request.method === 'GET' && path === '/admin/stats') {
    const token = request.headers.get('Authorization')?.match(/^Bearer ([a-f0-9]{64})$/)?.[1];
    if (!token || !await env.DB.prepare('SELECT token FROM sessions WHERE token=? AND expires>?').bind(await digest(token), now).first()) return json({ error: '다시 로그인해주세요.' }, 401);
    const day = new Date(Date.now() + 9 * 3600000).toISOString().slice(0, 10);
    const total = await env.DB.prepare('SELECT COALESCE(SUM(views),0) AS n FROM visits').first();
    const today = await env.DB.prepare('SELECT COALESCE(SUM(views),0) AS views, COUNT(*) AS visitors FROM visits WHERE day=?').bind(day).first();
    const comments = await env.DB.prepare('SELECT COUNT(*) AS n FROM comments').first();
    const { results } = await env.DB.prepare("SELECT day,SUM(views) AS views,COUNT(*) AS visitors FROM visits WHERE day >= ? GROUP BY day ORDER BY day DESC").bind(new Date(Date.now() + 9 * 3600000 - 29 * 86400000).toISOString().slice(0,10)).all();
    return json({ total: total.n, today: today.views, visitors: today.visitors, comments: comments.n, days: results });
  }
  if (request.method !== 'POST' || !['/visit','/comments','/admin/login'].includes(path)) return json({ error: '찾을 수 없습니다.' }, 404);
  if (!request.headers.get('Content-Type')?.includes('application/json')) return json({ error: 'JSON 요청이 필요합니다.' }, 415);
  const raw = await request.text();
  if (raw.length > 12000) return json({ error: '입력 내용이 너무 깁니다.' }, 413);
  let body; try { body = JSON.parse(raw); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
  if (!body || typeof body !== 'object') return json({ error: '잘못된 요청입니다.' }, 400);
  if (path === '/admin/login') {
    if (await limited(env, 'login:' + ip, 5, 900)) return json({ error: '로그인 시도가 많습니다. 15분 후 다시 시도해주세요.' }, 429);
    const given = await digest(typeof body.password === 'string' ? body.password : '');
    const expected = await digest(env.ADMIN_PASSWORD);
    let difference = 0; for (let i=0;i<expected.length;i++) difference |= given.charCodeAt(i)^expected.charCodeAt(i);
    if (difference) return json({ error: '비밀번호가 올바르지 않습니다.' }, 401);
    const token = [...crypto.getRandomValues(new Uint8Array(32))].map(b=>b.toString(16).padStart(2,'0')).join('');
    await env.DB.prepare('INSERT INTO sessions(token,expires) VALUES (?,?)').bind(await digest(token), now + 1800).run();
    return json({ token });
  }
  if (path === '/comments') {
    const name = typeof body.name === 'string' ? body.name.trim() || '익명' : '익명';
    const message = typeof body.message === 'string' ? body.message.trim() : '';
    if (name.length > 40 || message.length < 5 || message.length > 2000) return json({ error: '이름은 40자 이하, 피드백은 5~2,000자로 입력해주세요.' }, 400);
    if (await limited(env, 'comment:' + ip, 3, 600)) return json({ error: '잠시 후 다시 남겨주세요. 10분에 3개까지 작성할 수 있습니다.' }, 429);
    await env.DB.prepare('INSERT INTO comments(name,message,created_at) VALUES (?,?,?)').bind(name,message,new Date().toISOString()).run();
    return json({ ok: true }, 201);
  }
  if (typeof body.visitor !== 'string' || !/^[a-f0-9-]{36}$/i.test(body.visitor)) return json({ error: '잘못된 방문 정보입니다.' }, 400);
  if (await limited(env, 'visit:' + ip, 120, 600)) return json({ error: '요청이 많습니다.' }, 429);
  const day = new Date(Date.now() + 9 * 3600000).toISOString().slice(0,10);
  await env.DB.prepare('INSERT INTO visits(day,visitor,views) VALUES (?,?,1) ON CONFLICT(day,visitor) DO UPDATE SET views=views+1').bind(day, await digest(body.visitor)).run();
  return json({ ok: true });
}
export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get('Origin');
    const headers = { 'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN, 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, Authorization', 'Vary': 'Origin', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
    if (origin && origin !== env.ALLOWED_ORIGIN) return json({ error: '허용되지 않은 출처입니다.' }, 403);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
    try {
      const response = await route(request, env);
      return new Response(response.body, { status: response.status, headers: { ...Object.fromEntries(response.headers), ...headers } });
    } catch { return new Response(JSON.stringify({ error: '서버에 연결하지 못했습니다. 잠시 후 다시 시도해주세요.' }), { status: 500, headers: { ...headers, 'Content-Type': 'application/json' } }); }
  },
  async scheduled(event, env) {
    const now = Math.floor(Date.now()/1000);
    await env.DB.batch([env.DB.prepare('DELETE FROM sessions WHERE expires<=?').bind(now), env.DB.prepare('DELETE FROM limits WHERE expires<=?').bind(now)]);
  }
};
