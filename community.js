(() => {
  const base = (window.PORTFOLIO_API_URL || '').replace(/\/$/, '');
  const $ = id => document.getElementById(id);
  let token = '';
  async function api(path, options = {}) {
    if (!base) throw new Error('통계 기능을 준비 중입니다. 잠시 후 다시 시도해주세요.');
    const response = await fetch(base + path, { ...options, headers: { 'Content-Type': 'application/json', ...options.headers }, signal: AbortSignal.timeout(12000) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '요청을 처리하지 못했습니다. 다시 시도해주세요.');
    return data;
  }
  function logout() { token = ''; $('admin-password').value = ''; $('admin-stats').replaceChildren(); $('admin-stats').hidden = true; $('admin-logout').hidden = true; $('admin-login').hidden = false; $('admin-status').textContent = ''; }
  $('admin-open').onclick = () => { logout(); $('admin-dialog').showModal(); };
  $('admin-close').onclick = () => $('admin-dialog').close();
  $('admin-dialog').addEventListener('close', logout);
  $('admin-logout').onclick = logout;
  $('admin-login').onsubmit = async event => {
    event.preventDefault(); const button = event.target.querySelector('button'); button.disabled = true;
    try {
      const login = await api('/admin/login', { method: 'POST', body: JSON.stringify({ password: $('admin-password').value }) });
      token = login.token; $('admin-password').value = '';
      const stats = await api('/admin/stats', { headers: { Authorization: 'Bearer ' + token } });
      const description = document.createElement('p');
      description.textContent = `누적 조회 ${stats.total}회 · 오늘 조회 ${stats.today}회 · 오늘 방문 ${stats.visitors}회`;
      const note = document.createElement('p'); note.className = 'analytics-note';
      note.textContent = '한국 시간 기준 · 방문 수는 같은 브라우저의 하루 중복 방문을 제외한 추정치입니다. 브라우저 저장소 차단·기기 변경·봇 등에 따라 실제 인원과 다를 수 있습니다. 관리자 화면 조회는 집계하지 않습니다. 최근 30일을 표시합니다.';
      const table = document.createElement('table'); const head = table.createTHead().insertRow();
      ['날짜', '조회 수', '방문 수'].forEach(text => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = text; head.append(th); });
      const body = table.createTBody();
      stats.days.forEach(day => { const row = body.insertRow(); [day.day, day.views, day.visitors].forEach(value => { row.insertCell().textContent = value; }); });
      $('admin-stats').replaceChildren(description, note, table); $('admin-stats').hidden = false; $('admin-login').hidden = true; $('admin-logout').hidden = false; $('admin-status').textContent = '';
    } catch (e) { logout(); $('admin-status').textContent = e.message; }
    finally { button.disabled = false; }
  };
  if (!base) return;
  // A daily random browser identifier is used only to estimate same-day visits.
  const day = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  let visitor;
  try { const saved = JSON.parse(localStorage.getItem('portfolio-visitor') || 'null'); visitor = saved?.day === day ? saved.id : crypto.randomUUID(); localStorage.setItem('portfolio-visitor', JSON.stringify({ day, id: visitor })); } catch { visitor = crypto.randomUUID(); }
  api('/visit', { method: 'POST', body: JSON.stringify({ visitor }) }).catch(() => {});
})();
