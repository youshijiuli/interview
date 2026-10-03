#!/usr/bin/env node
/**
 * 知识库本地管理服务 (kb-server)
 * - 静态托管 manage.html
 * - CRUD API：读取/新建/保存/删除（删除移至 archive/，不真删）
 * - 一键重建 index.html（调用 build.js）
 * - 一键 Git 提交并推送双远端（origin=Gitee, github=GitHub）
 *
 * 启动：node server.js  然后浏览器打开 http://localhost:8877
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

const KB_ROOT = __dirname;                    // 仓库根（interview）
const ARCHIVE_DIR = path.join(KB_ROOT, 'archive');
const BUILD_JS = process.env.KB_BUILD_JS || 'C:\\Users\\ZhuanZ\\Doubao\\chats\\2026-10-03\\new-chat\\kb-builder\\build.js';
const PORT = Number(process.env.KB_PORT || 8877);

if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });

/* ---------- 工具 ---------- */
function safeResolve(p) {
  // 防目录穿越：只允许 KB_ROOT 内
  const target = path.resolve(KB_ROOT, p || '');
  if (target !== KB_ROOT && !target.startsWith(KB_ROOT + path.sep)) return null;
  return target;
}

function readTree(dir, base) {
  const out = [];
  let ents;
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return out; }
  ents.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN', { numeric: true }));
  for (const ent of ents) {
    if (ent.name === '.git' || ent.name === '.obsidian' || ent.name === 'archive' ||
        ent.name === 'node_modules' || ent.name === '.comc' || ent.name === 'fetch-repos' ||
        ent.name === 'kb-builder' || ent.name.startsWith('.') || ent.name === 'manage.html' ||
        ent.name === 'server.js' || ent.name === 'start-manage.bat') continue;
    const full = path.join(dir, ent.name);
    const rel = path.relative(KB_ROOT, full).split(path.sep).join('/');
    if (ent.isDirectory()) {
      const children = readTree(full, base);
      if (children.length) out.push({ type: 'dir', name: ent.name, path: rel, children });
    } else if (ent.isFile() && /\.(md|html)$/i.test(ent.name)) {
      let st;
      try { st = fs.statSync(full); } catch (e) { continue; }
      out.push({ type: 'file', name: ent.name, path: rel, size: st.size, mtime: st.mtime.toISOString().slice(0, 16).replace('T', ' ') });
    }
  }
  return out;
}

function run(cmd, args, cwd) {
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', timeout: 180000 });
  return { code: r.status === null ? -1 : r.status, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
}

/* ---------- HTTP ---------- */
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8' };

function send(res, code, body, type) {
  res.writeHead(code, { 'Content-Type': type || 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
  res.end(body);
}

function body(req) {
  return new Promise((resolve) => {
    let d = '';
    req.on('data', (c) => { d += c; if (d.length > 20 * 1024 * 1024) req.destroy(); });
    req.on('end', () => resolve(d));
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const p = url.pathname;

  /* ---- 静态 ---- */
  if (p === '/' || p === '/index.html') {
    const f = path.join(KB_ROOT, 'manage.html');
    if (fs.existsSync(f)) return send(res, 200, fs.readFileSync(f), 'text/html; charset=utf-8');
    return send(res, 404, 'manage.html not found');
  }

  /* ---- API ---- */
  if (p === '/api/tree' && req.method === 'GET') {
    return send(res, 200, JSON.stringify(readTree(KB_ROOT)));
  }
  if (p === '/api/doc' && req.method === 'GET') {
    const target = safeResolve(url.searchParams.get('path') || '');
    if (!target || !fs.existsSync(target) || !fs.statSync(target).isFile()) return send(res, 404, JSON.stringify({ error: 'not found' }));
    return send(res, 200, JSON.stringify({ content: fs.readFileSync(target, 'utf8') }));
  }
  if (p === '/api/doc' && (req.method === 'PUT' || req.method === 'POST')) {
    const raw = await body(req);
    let data; try { data = JSON.parse(raw); } catch (e) { return send(res, 400, JSON.stringify({ error: 'bad json' })); }
    const rel = data.path || '';
    if (!/\.md$/i.test(rel)) return send(res, 400, JSON.stringify({ error: 'only .md allowed' }));
    const target = safeResolve(rel);
    if (!target) return send(res, 400, JSON.stringify({ error: 'bad path' }));
    if (req.method === 'POST' && fs.existsSync(target)) return send(res, 409, JSON.stringify({ error: 'already exists' }));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, data.content, 'utf8');
    return send(res, 200, JSON.stringify({ ok: true, path: rel }));
  }
  if (p === '/api/doc' && req.method === 'DELETE') {
    const rel = url.searchParams.get('path') || '';
    const target = safeResolve(rel);
    if (!target || !fs.existsSync(target) || !fs.statSync(target).isFile()) return send(res, 404, JSON.stringify({ error: 'not found' }));
    // 移到 archive/，保留原名（重名则加序号）
    const base = path.basename(target);
    let dest = path.join(ARCHIVE_DIR, base);
    let i = 1;
    while (fs.existsSync(dest)) { dest = path.join(ARCHIVE_DIR, base.replace(/(\.[^.]+)$/, '-' + (i++) + '$1')); }
    fs.renameSync(target, dest);
    return send(res, 200, JSON.stringify({ ok: true, movedTo: path.relative(KB_ROOT, dest).split(path.sep).join('/') }));
  }
  if (p === '/api/build' && req.method === 'POST') {
    if (!fs.existsSync(BUILD_JS)) return send(res, 500, JSON.stringify({ error: 'build.js not found: ' + BUILD_JS }));
    const r = run(process.execPath, [BUILD_JS], path.dirname(BUILD_JS));
    const last = r.out.split('\n').filter(Boolean).slice(-3).join(' | ');
    return send(res, r.code === 0 ? 200 : 500, JSON.stringify({ ok: r.code === 0, detail: r.code === 0 ? last : (r.err || r.out).slice(0, 500) }));
  }
  if (p === '/api/git' && req.method === 'POST') {
    const raw = await body(req);
    let msg = 'kb: update';
    try { msg = (JSON.parse(raw).message || msg); } catch (e) {}
    const r1 = run('git', ['add', '-A'], KB_ROOT);
    const r2 = run('git', ['commit', '-m', msg], KB_ROOT);
    const r3 = run('git', ['push', 'github', 'master'], KB_ROOT);
    const r4 = run('git', ['push', 'origin', 'master'], KB_ROOT);
    return send(res, 200, JSON.stringify({
      ok: r3.code === 0 && r4.code === 0,
      add: { code: r1.code, out: r1.out, err: r1.err },
      commit: { code: r2.code, out: r2.out, err: r2.err },
      pushGithub: { code: r3.code, out: r3.out, err: r3.err },
      pushGitee: { code: r4.code, out: r4.out, err: r4.err }
    }));
  }
  if (p === '/api/git-status' && req.method === 'GET') {
    const r = run('git', ['status', '--short'], KB_ROOT);
    return send(res, 200, JSON.stringify({ dirty: r.out ? r.out.split('\n').filter(Boolean) : [] }));
  }

  return send(res, 404, JSON.stringify({ error: 'no route ' + p }));
});

server.listen(PORT, () => {
  console.log('');
  console.log('  知识库管理服务已启动');
  console.log('  ─────────────────────────────');
  console.log('  本机访问:  http://localhost:' + PORT);
  console.log('  按 Ctrl+C 停止服务');
  console.log('');
});
