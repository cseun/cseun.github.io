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
test('comment endpoints are disabled',async()=>{const {call}=setup();assert.equal((await call('/comments')).status,404);assert.equal((await call('/comments',{message:'hello'})).status,404);});
test('visits count views separately from daily visitors; rejects foreign origins',async()=>{
 const {call}=setup(); const visitor='12345678-1234-1234-1234-123456789abc';
 await call('/visit',{visitor}); await call('/visit',{visitor});
 const login=await call('/admin/login',{password:'test-password'});
 const stats=(await call('/admin/stats',undefined,login.data.token)).data;
 assert.equal(stats.total,2); assert.equal(stats.visitors,1); assert.equal(stats.today,2);
 assert.equal((await call('/admin/stats',undefined,undefined,'https://other.example')).status,403);
});
test('login is throttled',async()=>{const {call}=setup();for(let i=0;i<5;i++)assert.equal((await call('/admin/login',{password:'wrong'})).status,401);assert.equal((await call('/admin/login',{password:'test-password'})).status,429);});
