(() => {
  const base = (window.PORTFOLIO_API_URL || '').replace(/\/$/, '');
  const $ = id => document.getElementById(id);
  let cursor = null;
  let token = '';
  async function api(path, options = {}) {
    if (!base) throw new Error('댓글 기능을 준비 중입니다. 잠시 후 다시 방문해주세요.');
    const response = await fetch(base + path, { ...options, headers: { 'Content-Type': 'application/json', ...options.headers }, signal: AbortSignal.timeout(12000) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '요청을 처리하지 못했습니다. 다시 시도해주세요.');
    return data;
  }
  function entry(item) {
    const article = document.createElement('article'); article.className = 'feedback-entry';
    const name = document.createElement('strong'); name.textContent = item.name;
    const time = document.createElement('time'); time.dateTime = item.created_at;
    time.textContent = new Date(item.created_at).toLocaleDateString('ko-KR', { timeZone: 'Asia/Seoul' });
    const message = document.createElement('p'); message.textContent = item.message;
    article.append(name, time, message); return article;
  }
  async function load(more = false) {
    const data = await api('/comments' + (more && cursor ? '?before=' + cursor : ''));
    if (!more) $('feedback-list').replaceChildren();
    data.comments.forEach(item => $('feedback-list').append(entry(item)));
    cursor = data.next; $('feedback-more').hidden = !cursor;
    $('feedback-status').textContent = $('feedback-list').children.length ? '' : '첫 번째 피드백을 남겨주세요.';
  }
  $('feedback-more').onclick = async () => {
    $('feedback-more').disabled = true;
    try { await load(true); } catch (e) { $('feedback-status').textContent = e.message; }
    finally { $('feedback-more').disabled = false; }
  };
  $('feedback-form').onsubmit = async event => {
    event.preventDefault(); const button = event.target.querySelector('button'); button.disabled = true;
    try {
      await api('/comments', { method: 'POST', body: JSON.stringify({ name: $('feedback-name').value, message: $('feedback-message').value }) });
      event.target.reset();
      try { await load(); } catch { /* Saved feedback remains saved even if reloading fails. */ }
      $('feedback-status').textContent = '감사합니다. 남겨주신 피드백을 확인하고 개선에 반영하겠습니다.';
    } catch (e) { $('feedback-status').textContent = e.message; }
    finally { button.disabled = false; }
  };
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
      description.textContent = `누적 조회 ${stats.total}회 · 오늘 조회 ${stats.today}회 · 오늘 방문 ${stats.visitors}회 · 댓글 ${stats.comments}개`;
      const note = document.createElement('p'); note.className = 'feedback-note';
      note.textContent = '한국 시간 기준 · 방문 수는 같은 브라우저의 하루 중복 방문을 제외한 추정치입니다. 브라우저 저장소 차단·기기 변경·봇 등에 따라 실제 인원과 다를 수 있습니다. 관리자 화면 조회는 집계하지 않습니다. 최근 30일을 표시합니다.';
      const table = document.createElement('table'); const head = table.createTHead().insertRow();
      ['날짜', '조회 수', '방문 수'].forEach(text => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = text; head.append(th); });
      const body = table.createTBody();
      stats.days.forEach(day => { const row = body.insertRow(); [day.day, day.views, day.visitors].forEach(value => { row.insertCell().textContent = value; }); });
      $('admin-stats').replaceChildren(description, note, table); $('admin-stats').hidden = false; $('admin-login').hidden = true; $('admin-logout').hidden = false; $('admin-status').textContent = '';
    } catch (e) { logout(); $('admin-status').textContent = e.message; }
    finally { button.disabled = false; }
  };
  load().catch(e => { $('feedback-status').textContent = e.message; });
  if (!base) { $('feedback-form').querySelector('button').disabled = true; return; }
  // A daily random browser identifier is used only to estimate same-day visits.
  const day = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  let visitor;
  try { const saved = JSON.parse(localStorage.getItem('portfolio-visitor') || 'null'); visitor = saved?.day === day ? saved.id : crypto.randomUUID(); localStorage.setItem('portfolio-visitor', JSON.stringify({ day, id: visitor })); } catch { visitor = crypto.randomUUID(); }
  api('/visit', { method: 'POST', body: JSON.stringify({ visitor }) }).catch(() => {});
})();
