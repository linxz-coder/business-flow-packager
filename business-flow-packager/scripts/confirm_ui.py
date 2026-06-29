#!/usr/bin/env python3
"""Local browser confirmation page for business-flow packaging decisions."""

from __future__ import annotations

import argparse
import json
import socket
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


CONFIRM_DIR = "confirm_ui"
RECOMMENDATIONS_FILE = "recommendations.json"
RESULT_FILE = "result.json"
DEFAULT_PORT = 5050
WAIT_TIMEOUT_DEFAULT = 590


HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Business Flow Packager - Confirm</title>
  <style>
    :root { color-scheme: light; --ink:#111827; --muted:#667085; --line:#d0d5dd; --bg:#f6f7f9; --panel:#fff; --brand:#0f766e; }
    * { box-sizing: border-box; }
    body { margin:0; font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"PingFang SC","Microsoft YaHei",sans-serif; color:var(--ink); background:var(--bg); }
    header { position:sticky; top:0; z-index:5; background:rgba(255,255,255,.96); border-bottom:1px solid var(--line); }
    .wrap { max-width:980px; margin:0 auto; padding:20px; }
    h1 { margin:0 0 4px; font-size:22px; }
    h2 { margin:28px 0 12px; font-size:17px; }
    p { margin:6px 0; }
    .muted { color:var(--muted); }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; margin:14px 0; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:12px; }
    .option { display:block; border:1px solid var(--line); border-radius:8px; padding:12px; cursor:pointer; background:#fff; min-height:82px; }
    .option input { margin-right:8px; }
    .option:has(input:checked) { border-color:var(--brand); box-shadow:0 0 0 2px rgba(15,118,110,.12); }
    label strong { display:inline-block; margin-bottom:3px; }
    textarea, input[type=text] { width:100%; border:1px solid var(--line); border-radius:8px; padding:10px; font:inherit; background:#fff; }
    textarea { min-height:92px; resize:vertical; }
    ul { margin:8px 0 0 20px; padding:0; }
    code { background:#eef2f7; padding:2px 5px; border-radius:5px; }
    footer { position:sticky; bottom:0; border-top:1px solid var(--line); background:rgba(255,255,255,.97); }
    button { border:0; border-radius:8px; background:var(--brand); color:#fff; font-weight:650; font-size:15px; padding:11px 18px; cursor:pointer; }
    button.secondary { background:#344054; }
    .actions { display:flex; gap:10px; align-items:center; justify-content:flex-end; }
    .status { margin-right:auto; color:var(--muted); }
    .pill { display:inline-block; border:1px solid var(--line); border-radius:999px; padding:2px 8px; margin:3px 4px 3px 0; color:#344054; background:#fff; }
    .risk { border-color:#fecdca; background:#fff7f6; }
    .hidden { display:none; }
  </style>
</head>
<body>
  <header><div class="wrap">
    <h1 id="title">Business Flow Packager</h1>
    <p id="subtitle" class="muted">确认少数打包决策后，AI 会继续自动完成脚本和交付包。</p>
  </div></header>
  <main class="wrap">
    <section class="card">
      <h2>本次要打包的流程</h2>
      <p id="summary"></p>
      <div id="evidence"></div>
    </section>
    <section id="risk-section" class="card risk hidden">
      <h2>需要你确认的风险</h2>
      <ul id="risks"></ul>
    </section>
    <section id="decisions"></section>
  </main>
  <footer><div class="wrap actions">
    <span id="status" class="status">等待确认</span>
    <button class="secondary" id="btn-copy">复制当前选择</button>
    <button id="btn-confirm">确认并继续</button>
  </div></footer>
  <script>
    const state = { rec: null, values: {} };
    const $ = (id) => document.getElementById(id);

    function escapeHtml(s) {
      return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }
    function setValue(id, value) { state.values[id] = value; }
    function renderList(items) {
      if (!items || !items.length) return '';
      return '<ul>' + items.map(item => '<li>' + escapeHtml(item) + '</li>').join('') + '</ul>';
    }
    function renderDecision(decision) {
      const id = decision.id;
      const type = decision.type || 'choice';
      const current = decision.default ?? decision.value ?? '';
      setValue(id, current);
      let body = '';
      if (type === 'choice') {
        body = '<div class="grid">' + (decision.options || []).map(opt => {
          const checked = String(opt.value) === String(current) ? 'checked' : '';
          return `<label class="option"><input type="radio" name="${escapeHtml(id)}" value="${escapeHtml(opt.value)}" ${checked}>
            <strong>${escapeHtml(opt.label || opt.value)}</strong><br><span class="muted">${escapeHtml(opt.description || '')}</span></label>`;
        }).join('') + '</div>';
      } else if (type === 'multi_choice') {
        const selected = new Set(Array.isArray(current) ? current : []);
        setValue(id, Array.from(selected));
        body = '<div class="grid">' + (decision.options || []).map(opt => {
          const checked = selected.has(opt.value) ? 'checked' : '';
          return `<label class="option"><input type="checkbox" name="${escapeHtml(id)}" value="${escapeHtml(opt.value)}" ${checked}>
            <strong>${escapeHtml(opt.label || opt.value)}</strong><br><span class="muted">${escapeHtml(opt.description || '')}</span></label>`;
        }).join('') + '</div>';
      } else if (type === 'boolean') {
        setValue(id, Boolean(current));
        body = `<label class="option"><input type="checkbox" name="${escapeHtml(id)}" ${current ? 'checked' : ''}> ${escapeHtml(decision.true_label || '确认')}</label>`;
      } else {
        body = `<textarea name="${escapeHtml(id)}">${escapeHtml(current)}</textarea>`;
      }
      return `<section class="card" data-decision="${escapeHtml(id)}"><h2>${escapeHtml(decision.label || id)}</h2>
        <p class="muted">${escapeHtml(decision.description || '')}</p>${body}</section>`;
    }
    function bindDecision(decision) {
      const id = decision.id;
      const type = decision.type || 'choice';
      document.querySelectorAll(`[name="${CSS.escape(id)}"]`).forEach(el => {
        el.addEventListener('change', () => {
          if (type === 'multi_choice') {
            setValue(id, Array.from(document.querySelectorAll(`[name="${CSS.escape(id)}"]:checked`)).map(x => x.value));
          } else if (type === 'boolean') {
            setValue(id, el.checked);
          } else {
            setValue(id, el.value);
          }
        });
        el.addEventListener('input', () => setValue(id, el.value));
      });
    }
    async function load() {
      const response = await fetch('/api/recommendations', { cache: 'no-store' });
      state.rec = await response.json();
      $('title').textContent = state.rec.title || 'Business Flow Packager';
      $('summary').textContent = state.rec.summary || 'AI 已根据成功 session 生成默认打包方案。';
      $('subtitle').textContent = state.rec.hint || $('subtitle').textContent;
      const evidence = state.rec.evidence || {};
      const chips = [];
      for (const [key, value] of Object.entries(evidence)) {
        if (Array.isArray(value)) value.forEach(v => chips.push(`<span class="pill">${escapeHtml(key)}: ${escapeHtml(v)}</span>`));
        else if (value) chips.push(`<span class="pill">${escapeHtml(key)}: ${escapeHtml(value)}</span>`);
      }
      $('evidence').innerHTML = chips.join('');
      const risks = state.rec.risks || [];
      if (risks.length) {
        $('risk-section').classList.remove('hidden');
        $('risks').innerHTML = risks.map(r => `<li>${escapeHtml(r)}</li>`).join('');
      }
      $('decisions').innerHTML = (state.rec.decisions || []).map(renderDecision).join('');
      (state.rec.decisions || []).forEach(bindDecision);
    }
    async function confirm() {
      $('status').textContent = '正在保存...';
      const payload = { status: 'confirmed', values: state.values, recommendations: state.rec };
      const response = await fetch('/api/confirm', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      if (!response.ok) throw new Error(await response.text());
      $('status').textContent = '已确认，可以回到 AI 对话窗口。';
      $('btn-confirm').disabled = true;
    }
    $('btn-confirm').addEventListener('click', () => confirm().catch(err => $('status').textContent = '保存失败: ' + err.message));
    $('btn-copy').addEventListener('click', async () => {
      await navigator.clipboard.writeText(JSON.stringify(state.values, null, 2));
      $('status').textContent = '已复制当前选择';
    });
    load().catch(err => $('summary').textContent = '加载失败: ' + err.message);
  </script>
</body>
</html>
"""


def find_free_port(start: int) -> int:
    for port in range(start, start + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError(f"no free port found from {start}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_handler(project_path: Path, stop_event: threading.Event):
    confirm_dir = project_path / CONFIRM_DIR
    recommendations_file = confirm_dir / RECOMMENDATIONS_FILE
    result_file = confirm_dir / RESULT_FILE

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:
            return

        def send_json(self, data: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/":
                body = HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if parsed.path == "/api/recommendations":
                self.send_json(load_json(recommendations_file))
                return
            self.send_error(404)

        def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/api/confirm":
                self.send_error(404)
                return
            length = int(self.headers.get("Content-Length", "0"))
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except json.JSONDecodeError as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            payload["status"] = "confirmed"
            payload["confirmed_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            write_json(result_file, payload)
            self.send_json({"ok": True, "result": str(result_file)})
            threading.Timer(0.5, stop_event.set).start()

    return Handler


def write_sample(project_path: Path) -> Path:
    recommendations = {
        "title": "确认业务流打包方案",
        "summary": "AI 已从成功 session 提取默认方案。请只确认少数会影响交付方式的决策。",
        "hint": "确认后 AI 会继续生成脚本、验证并整理交付包。",
        "evidence": {
            "source": "current-session",
            "outputs": ["exports/report.xlsx"],
            "verified": ["dry-run ok"],
        },
        "risks": ["示例风险：脚本面板入口会在你确认后才添加。"],
        "decisions": [
            {
                "id": "delivery",
                "label": "交付形式",
                "description": "默认选择最适合当前 session 的形式。",
                "type": "multi_choice",
                "default": ["script", "handoff"],
                "options": [
                    {"value": "script", "label": "一键脚本", "description": "生成可重复运行的脚本。"},
                    {"value": "panel", "label": "脚本面板候选", "description": "生成候选按钮，用户确认后再加入面板。"},
                    {"value": "handoff", "label": "办公交付包", "description": "整理给同事使用的说明、配置样例和验证步骤。"},
                ],
            },
            {
                "id": "platform",
                "label": "平台",
                "description": "只有在流程可移植时才选择 Windows exe。",
                "type": "choice",
                "default": "mac",
                "options": [
                    {"value": "mac", "label": "macOS", "description": "脚本 + 可选 app 包装。"},
                    {"value": "cross-platform", "label": "跨平台", "description": "尽量避免系统专属依赖。"},
                    {"value": "windows", "label": "Windows exe", "description": "仅在无 Mac-only 依赖时使用。"},
                ],
            },
        ],
    }
    path = project_path / CONFIRM_DIR / RECOMMENDATIONS_FILE
    write_json(path, recommendations)
    return path


def serve(project_path: Path, port: int, open_browser: bool, wait_timeout: int) -> int:
    confirm_dir = project_path / CONFIRM_DIR
    recommendations_file = confirm_dir / RECOMMENDATIONS_FILE
    result_file = confirm_dir / RESULT_FILE
    if not recommendations_file.exists():
        raise SystemExit(f"missing {recommendations_file}; write recommendations before launching confirm UI")

    stop_event = threading.Event()
    actual_port = find_free_port(port)
    server = ThreadingHTTPServer(("127.0.0.1", actual_port), make_handler(project_path, stop_event))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{actual_port}/"
    print(url, flush=True)
    if open_browser:
        webbrowser.open(url)

    deadline = None if wait_timeout <= 0 else time.time() + wait_timeout
    try:
        while not stop_event.is_set():
            if result_file.exists():
                break
            if deadline is not None and time.time() >= deadline:
                print(f"timed out waiting for confirmation; page may still be open: {url}", flush=True)
                return 124
            time.sleep(0.25)
        return 0
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", help="Workflow package path containing confirm_ui/recommendations.json")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--wait-timeout", type=int, default=WAIT_TIMEOUT_DEFAULT)
    parser.add_argument("--init-sample", action="store_true", help="Write a sample recommendations.json and exit")
    args = parser.parse_args()

    project_path = Path(args.project_path).expanduser().resolve()
    if args.init_sample:
        print(write_sample(project_path))
        return 0
    return serve(project_path, port=args.port, open_browser=not args.no_browser, wait_timeout=args.wait_timeout)


if __name__ == "__main__":
    raise SystemExit(main())
