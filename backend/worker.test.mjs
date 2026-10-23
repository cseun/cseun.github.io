import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import worker from './worker.mjs';
function setup() {
  const db = new DatabaseSync(':memory:'); db.exec(readFileSync(new URL('./schema.sql', import.meta.url),'utf8'));
  const env = { ADMIN_PASSWORD: 'test-password', IP_SALT: 'test-salt', ALLOWED_ORIGIN: 'https://cseun.github.io', DB: { prepare(sql) { let values=[]; return { bind(...args) { values=args; return this; }, async first() { return db.prepare(sql).get(...values) || null; }, async all() { return { results: db.prepare(sql).all(...values) }; }, async run() { return db.prepare(sql).run(...values); } }; } } };
  async function call(path, body, token, origin=env.ALLOWED_ORIGIN) {
    const headers = { Origin:origin, 'Content-Type':'application/json', 'CF-Connecting-IP':'127.0.0.1' }; if(token) headers.Authorization='Bearer '+token;
    const res = await worker.fetch(new Request('https://api.example'+path, { method:body===undefined?'GET':'POST', headers, ...(body===undefined?{}:{body:JSON.stringify(body)}) }),env,{});
    return { status:res.status, data:await res.json() };
  }
  return { call, db };
}
test('private stats require server authentication and sessions expire', async()=>{
  const {call,db}=setup(); assert.equal((await call('/admin/stats')).status,401);
  assert.equal((await call('/admin/login',{password:'wrong'})).status,401);
  const login=await call('/admin/login',{password:'test-password'}); assert.equal(login.status,200);
  assert.equal((await call('/admin/stats',undefined,login.data.token)).status,200);
  db.exec('UPDATE sessions SET expires=0'); assert.equal((await call('/admin/stats',undefined,login.data.token)).status,401);
});
test('comments validate, paginate, preserve plain text and rate limit',async()=>{
 const {call,db}=setup(); assert.equal((await call('/comments',{message:'a'})).status,400);
 assert.equal((await call('/comments',{name:'',message:'<script>alert(1)</script>'})).status,201);
 assert.equal((await call('/comments')).data.comments[0].name,'익명');
 for(let i=0;i<25;i++) db.prepare('INSERT INTO comments(name,message,created_at) VALUES (?,?,?)').run('test','hello',new Date().toISOString());
 const first=(await call('/comments')).data; assert.equal(first.comments.length,20); assert.ok(first.next);
 const second=(await call('/comments?before='+first.next)).data; assert.equal(second.comments.length,6);
 await call('/comments',{message:'hello'}); await call('/comments',{message:'hello'});
 assert.equal((await call('/comments',{message:'hello'})).status,429);
});
test('visits count views separately from daily visitors; rejects foreign origins',async()=>{
 const {call}=setup(); const visitor='12345678-1234-1234-1234-123456789abc';
 await call('/visit',{visitor}); await call('/visit',{visitor});
 const login=await call('/admin/login',{password:'test-password'});
 const stats=(await call('/admin/stats',undefined,login.data.token)).data;
 assert.equal(stats.total,2); assert.equal(stats.visitors,1); assert.equal(stats.today,2);
 assert.equal((await call('/comments',undefined,undefined,'https://other.example')).status,403);
});
test('login is throttled',async()=>{const {call}=setup();for(let i=0;i<5;i++)assert.equal((await call('/admin/login',{password:'wrong'})).status,401);assert.equal((await call('/admin/login',{password:'test-password'})).status,429);});
