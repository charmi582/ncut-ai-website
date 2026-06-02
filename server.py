from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from http import cookies
from pathlib import Path
import json
import os
import secrets
import shutil
import time
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "site.json"
BACKUP_DIR = ROOT / "data" / "backups"
PASSWORD = os.environ.get("NCUT_ADMIN_PASSWORD", "ncutai")
SESSIONS = {}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.apply_response_headers()
        super().end_headers()

    def apply_response_headers(self):
        path = urlparse(self.path).path
        self.send_header("Cache-Control", cache_control_for_path(path))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header("Content-Security-Policy", content_security_policy())

    def do_GET(self):
        if self.path == "/api/site":
            self.json_response(read_site())
            return
        if self.path == "/api/status":
            self.json_response({"ok": True, "authenticated": self.is_authenticated()})
            return
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and self.command == "GET":
            page = ROOT / "404.html"
            if page.exists():
                payload = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
        super().send_error(code, message, explain)

    def do_POST(self):
        if self.path == "/api/login":
            body = self.read_json()
            if body.get("password") != PASSWORD:
                self.json_response({"ok": False, "message": "密碼錯誤"}, 401)
                return
            token = secrets.token_urlsafe(32)
            SESSIONS[token] = time.time()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Set-Cookie", f"ncut_admin={token}; Path=/; HttpOnly; SameSite=Lax")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8"))
            return

        if self.path == "/api/logout":
            token = self.session_token()
            if token in SESSIONS:
                del SESSIONS[token]
            self.json_response({"ok": True})
            return

        if self.path == "/api/site":
            if not self.is_authenticated():
                self.json_response({"ok": False, "message": "尚未登入"}, 401)
                return
            try:
                payload = self.read_json()
                validate_site(payload)
                backup_path = backup_site()
                DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
                self.json_response({
                    "ok": True,
                    "savedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "backup": backup_path.name
                })
            except Exception as error:
                self.json_response({"ok": False, "message": str(error)}, 400)
            return

        self.send_error(404)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(raw)

    def json_response(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def session_token(self):
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        morsel = jar.get("ncut_admin")
        return morsel.value if morsel else ""

    def is_authenticated(self):
        token = self.session_token()
        return bool(token and token in SESSIONS)


def read_site():
    return json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))


def validate_site(payload):
    required = ["identity", "contact", "hero", "pages", "faculty", "staff", "news", "videos"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))


def backup_site():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"site-{stamp}.json"
    shutil.copy2(DATA_FILE, backup_path)
    backups = sorted(BACKUP_DIR.glob("site-*.json"))
    for old_backup in backups[:-30]:
        old_backup.unlink(missing_ok=True)
    return backup_path


def cache_control_for_path(path):
    if path.startswith("/api/") or path.startswith("/data/"):
        return "no-store"
    if path in ("", "/") or path.endswith(".html"):
        return "no-cache, must-revalidate"
    if path.endswith((".css", ".js", ".webmanifest", ".xml", ".txt")):
        return "public, max-age=3600, stale-while-revalidate=86400"
    if path.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".mp4", ".woff", ".woff2")):
        return "public, max-age=604800, immutable"
    return "no-cache, must-revalidate"


def content_security_policy():
    return "; ".join([
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' https://n063.ncut.edu.tw https://ai.ncut.edu.tw https://i.ytimg.com data:",
        "media-src 'self'",
        "frame-src https://www.youtube.com https://www.youtube-nocookie.com",
        "connect-src 'self'",
        "font-src 'self' data:",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'self'",
        "upgrade-insecure-requests"
    ])


if __name__ == "__main__":
    os.chdir(ROOT)
    port = int(os.environ.get("PORT", "8080"))
    print(f"NCUT AI site running: http://localhost:{port}/")
    print(f"Admin UI: http://localhost:{port}/admin/  default password: {PASSWORD}")
    ThreadingHTTPServer(("localhost", port), Handler).serve_forever()
