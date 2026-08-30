from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from http import cookies
from pathlib import Path
from urllib.parse import urlparse
import base64
import json
import mimetypes
import os
import re
import secrets
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "site.json"
BACKUP_DIR = ROOT / "data" / "backups"
UPLOAD_DIR = ROOT / "assets" / "uploads"
PASSWORD = os.environ.get("NCUT_ADMIN_PASSWORD", "ncutai")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8080"))
SESSIONS = {}


class Handler(SimpleHTTPRequestHandler):
    server_version = "NCUTLocalCMS/1.0"

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
        path = urlparse(self.path).path
        if path == "/api/status":
            self.json_response({
                "ok": True,
                "authenticated": self.is_authenticated(),
                "localOnly": HOST in ("127.0.0.1", "localhost"),
                "host": HOST,
                "port": PORT
            })
            return
        if path == "/api/site":
            if not self.require_auth():
                return
            self.json_response(read_site())
            return
        if path == "/api/git/status":
            if not self.require_auth():
                return
            self.json_response({"ok": True, **git_status()})
            return
        if path == "/api/assets":
            if not self.require_auth():
                return
            self.json_response({"ok": True, "assets": list_assets()})
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
        path = urlparse(self.path).path
        if path == "/api/login":
            body = self.read_json()
            if not secrets.compare_digest(str(body.get("password", "")), PASSWORD):
                self.json_response({"ok": False, "message": "密碼錯誤"}, 401)
                return
            token = secrets.token_urlsafe(32)
            SESSIONS[token] = time.time()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Set-Cookie", f"ncut_admin={token}; Path=/; HttpOnly; SameSite=Strict")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8"))
            return

        if not self.require_auth():
            return
        if not self.require_local_request():
            return

        if path == "/api/logout":
            token = self.session_token()
            SESSIONS.pop(token, None)
            self.json_response({"ok": True})
            return
        if path == "/api/site":
            self.save_site()
            return
        if path == "/api/assets/upload":
            self.upload_asset()
            return
        if path == "/api/build":
            self.run_build()
            return
        if path == "/api/git/commit":
            self.git_commit()
            return
        if path == "/api/git/push":
            self.git_push()
            return
        self.send_error(404)

    def save_site(self):
        try:
            payload = self.read_json()
            validate_site(payload)
            backup_path = backup_site()
            DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.json_response({
                "ok": True,
                "savedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                "backup": backup_path.name
            })
        except Exception as error:
            self.json_response({"ok": False, "message": str(error)}, 400)

    def upload_asset(self):
        try:
            payload = self.read_json(max_bytes=20 * 1024 * 1024)
            asset = save_asset(payload)
            self.json_response({"ok": True, "asset": asset})
        except Exception as error:
            self.json_response({"ok": False, "message": str(error)}, 400)

    def run_build(self):
        result = run_command(["node", "scripts/build-pages.mjs"])
        self.json_response({"ok": result["code"] == 0, **result}, 200 if result["code"] == 0 else 400)

    def git_commit(self):
        body = self.read_json()
        message = str(body.get("message") or "").strip()
        if not message:
            self.json_response({"ok": False, "message": "請輸入 commit 訊息"}, 400)
            return
        add_result = run_command(["git", "add", "."])
        if add_result["code"] != 0:
            self.json_response({"ok": False, "step": "add", **add_result}, 400)
            return
        commit_result = run_command(["git", "commit", "-m", message])
        self.json_response({"ok": commit_result["code"] == 0, "step": "commit", **commit_result}, 200 if commit_result["code"] == 0 else 400)

    def git_push(self):
        result = run_command(["git", "push", "origin", "main"])
        self.json_response({"ok": result["code"] == 0, **result}, 200 if result["code"] == 0 else 400)

    def read_json(self, max_bytes=2 * 1024 * 1024):
        length = int(self.headers.get("Content-Length", "0"))
        if length > max_bytes:
            raise ValueError("request body too large")
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

    def require_auth(self):
        if self.is_authenticated():
            return True
        self.json_response({"ok": False, "message": "請先登入本地 CMS"}, 401)
        return False

    def require_local_request(self):
        origin = self.headers.get("Origin", "")
        if origin and not re.match(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$", origin):
            self.json_response({"ok": False, "message": "管理操作只接受本機來源"}, 403)
            return False
        return True


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


def save_asset(payload):
    name = safe_filename(payload.get("name", "asset"))
    data_url = str(payload.get("dataUrl", ""))
    match = re.match(r"^data:([^;]+);base64,(.+)$", data_url, re.S)
    if not match:
        raise ValueError("upload must use a data URL")
    mime_type, encoded = match.groups()
    extension = allowed_extension(name, mime_type)
    raw = base64.b64decode(encoded, validate=True)
    if len(raw) > 15 * 1024 * 1024:
        raise ValueError("asset is larger than 15 MB")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(name).stem[:70] or "asset"
    filename = f"{time.strftime('%Y%m%d-%H%M%S')}-{stem}{extension}"
    path = UPLOAD_DIR / filename
    path.write_bytes(raw)
    return {
        "path": f"./assets/uploads/{filename}",
        "name": filename,
        "type": mime_type,
        "size": len(raw)
    }


def safe_filename(value):
    name = Path(str(value)).name
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-") or "asset"


def allowed_extension(name, mime_type):
    allowed = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".mp4": "video/mp4",
        ".pdf": "application/pdf"
    }
    suffix = Path(name).suffix.lower()
    if suffix in allowed and allowed[suffix] == mime_type:
        return suffix
    guessed = mimetypes.guess_extension(mime_type) or ""
    if guessed in allowed:
        return guessed
    raise ValueError(f"unsupported asset type: {mime_type}")


def list_assets():
    assets = []
    if not (ROOT / "assets").exists():
        return assets
    for path in sorted((ROOT / "assets").rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        assets.append({
            "path": f"./{rel}",
            "name": path.name,
            "size": path.stat().st_size,
            "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(path.stat().st_mtime))
        })
    return assets


def git_status():
    result = run_command(["git", "status", "--short", "--branch"])
    return {
        "status": result["stdout"],
        "error": result["stderr"],
        "code": result["code"]
    }


def run_command(command):
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=120,
            shell=False
        )
        return {
            "code": completed.returncode,
            "stdout": completed.stdout[-12000:],
            "stderr": completed.stderr[-12000:]
        }
    except FileNotFoundError:
        return {"code": 127, "stdout": "", "stderr": f"command not found: {command[0]}"}
    except subprocess.TimeoutExpired as error:
        return {
            "code": 124,
            "stdout": (error.stdout or "")[-12000:],
            "stderr": "command timed out"
        }


def cache_control_for_path(path):
    if path.startswith("/api/") or path.startswith("/data/"):
        return "no-store"
    if path in ("", "/") or path.endswith(".html"):
        return "no-cache, must-revalidate"
    if path.endswith((".css", ".js", ".webmanifest", ".xml", ".txt")):
        return "public, max-age=3600, stale-while-revalidate=86400"
    if path.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".mp4", ".woff", ".woff2", ".pdf")):
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
    print(f"NCUT AI local CMS: http://{HOST}:{PORT}/admin/")
    print(f"Static preview: http://{HOST}:{PORT}/")
    print("Server is intended for local use only. Keep HOST=127.0.0.1 unless you know why it must change.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
