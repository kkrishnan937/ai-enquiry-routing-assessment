"""Local enquiry tracking demonstration. Python standard library only."""
import argparse
from contextlib import contextmanager
import datetime as dt
import hashlib
import hmac
import html
import json
import os
import secrets
import sqlite3
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VERSION = "0.1.1"
USERS = {"rep-a": "representative", "rep-b": "representative",
         "rep-c": "representative", "supervisor-a": "supervisor"}


class Error(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


class Store:
    def __init__(self, path, today=None):
        self.path, self.test_today = path, today
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.executescript('''
              CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY, role TEXT, salt TEXT, digest TEXT);
              CREATE TABLE IF NOT EXISTS enquiries(id TEXT PRIMARY KEY, body TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS history(seq INTEGER PRIMARY KEY AUTOINCREMENT,
                enquiry TEXT, actor TEXT, timestamp TEXT, field TEXT, old_value TEXT, new_value TEXT, reason TEXT);
            ''')

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def init_users(self):
        credentials = {}
        with self.db() as db:
            for name, role in USERS.items():
                if db.execute("SELECT 1 FROM users WHERE name=?", (name,)).fetchone():
                    continue
                password, salt = secrets.token_urlsafe(15), secrets.token_hex(16)
                digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 300000).hex()
                db.execute("INSERT INTO users VALUES(?,?,?,?)", (name, role, salt, digest))
                credentials[name] = password
        return credentials

    def authenticate(self, name, password):
        with self.db() as db:
            user = db.execute("SELECT * FROM users WHERE name=?", (name,)).fetchone()
        if not user:
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(user["salt"]), 300000).hex()
        return hmac.compare_digest(digest, user["digest"])

    def now(self):
        return dt.datetime.now(dt.timezone.utc).isoformat()

    def today(self):
        return self.test_today or dt.date.today().isoformat()

    def allowed(self, actor, record):
        return USERS.get(actor) == "supervisor" or actor in (record["responsible"], record["cover"])

    def get(self, db, actor, ref):
        row = db.execute("SELECT body FROM enquiries WHERE id=?", (ref,)).fetchone()
        if not row:
            raise Error(404, "Enquiry not found")
        record = json.loads(row["body"])
        if not self.allowed(actor, record):
            raise Error(403, "You do not have access to this enquiry")
        return record

    def validate(self, record):
        if record.get("responsible") not in USERS or USERS[record["responsible"]] != "representative":
            raise Error(400, "A named responsible representative is required")
        try:
            dt.date.fromisoformat(record["follow_up"])
        except (ValueError, KeyError, TypeError):
            raise Error(400, "A valid follow-up date is required")
        if not record.get("message", "").strip():
            raise Error(400, "An enquiry message is required")
        received = record.get("received")
        if not isinstance(received, str) or not received.strip():
            raise Error(400, "Received time is required")
        record["received"] = received.strip()
        try:
            stamp = dt.datetime.fromisoformat(record["received"])
        except ValueError:
            raise Error(400, "Received time must be a valid date and time, for example 2026-11-12T09:00:00-06:00")
        if stamp.tzinfo is None:
            raise Error(400, "Received time must include its time zone, for example -06:00")

    def event(self, db, ref, actor, field, old, new, reason=""):
        db.execute("INSERT INTO history(enquiry,actor,timestamp,field,old_value,new_value,reason) VALUES(?,?,?,?,?,?,?)",
                   (ref, actor, self.now(), field, json.dumps(old), json.dumps(new), reason))

    def list_records(self, actor, search=""):
        with self.db() as db:
            records = [json.loads(row[0]) for row in db.execute("SELECT body FROM enquiries")]
        return [r for r in records if self.allowed(actor, r) and (not search or r["id"] == search)]

    def read(self, actor, ref):
        with self.db() as db:
            record = self.get(db, actor, ref)
            history = [dict(row) for row in db.execute("SELECT * FROM history WHERE enquiry=? ORDER BY seq", (ref,))]
        return {**record, "history": history, "overdue": record["follow_up"] < self.today()}

    def create(self, actor, data):
        record = {"id": "ENQ-" + secrets.token_hex(6).upper(), "received": data.get("received", ""),
                  "message": data.get("message", ""), "responsible": data.get("responsible", ""),
                  "cover": None, "missing": data.get("missing", ""), "address": "",
                  "last_action": data.get("last_action", ""), "next_action": data.get("next_action", ""),
                  "follow_up": data.get("follow_up", ""), "state": "Open", "messages": []}
        self.validate(record)
        if USERS[actor] != "supervisor" and record["responsible"] != actor:
            raise Error(403, "Representatives may create only their own enquiries")
        record["messages"].append({"direction": "incoming", "text": record["message"], "recorded": self.now()})
        with self.db() as db:
            db.execute("INSERT INTO enquiries VALUES(?,?)", (record["id"], json.dumps(record)))
            self.event(db, record["id"], actor, "created", None, record)
        return record

    def change(self, actor, ref, action, data):
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            record = self.get(db, actor, ref)
            before = json.loads(json.dumps(record))
            reason = ""
            if action == "update":
                permitted = {"missing", "address", "last_action", "next_action", "follow_up"}
                if set(data) - permitted:
                    raise Error(400, "Use the authorised cover or transfer action for assignment changes")
                record.update(data)
            elif action == "message":
                if data.get("direction") not in ("incoming", "outgoing") or not data.get("text", "").strip():
                    raise Error(400, "Message direction and text are required")
                record["messages"].append({"direction": data["direction"], "text": data["text"], "recorded": self.now()})
            elif action in ("cover", "transfer"):
                if USERS[actor] != "supervisor":
                    raise Error(403, "Only the supervisor may change assignments")
                target = data.get("representative") or None
                if target is not None and (target not in USERS or USERS[target] != "representative"):
                    raise Error(400, "Select a valid representative")
                if action == "cover":
                    if target == record["responsible"]:
                        raise Error(400, "Cover must differ from the responsible representative")
                    record["cover"] = target
                else:
                    reason = data.get("reason", "").strip()
                    if not target or not reason or data.get("confirmed") is not True:
                        raise Error(400, "Receiving representative, reason and confirmation are required")
                    if target == record["responsible"]:
                        raise Error(400, "Choose a different responsible representative")
                    # Reject ambiguity instead of silently altering temporary cover.
                    if record["cover"]:
                        raise Error(400, "Remove temporary cover before permanent transfer")
                    record["responsible"] = target
            else:
                raise Error(405, "Action is not supported")
            self.validate(record)
            for field, value in record.items():
                if before[field] != value:
                    self.event(db, ref, actor, field, before[field], value, reason)
            db.execute("UPDATE enquiries SET body=? WHERE id=?", (json.dumps(record), ref))
        return record


def page(title, body, csrf=""):
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
    <title>{html.escape(title)} — Enquiry tracking</title><style>
    body{{font:16px system-ui;max-width:1050px;margin:35px auto;padding:0 24px;color:#183047;background:#f5f7fa}}
    header,section{{background:white;padding:24px;border-radius:10px;margin-bottom:18px;border:1px solid #d6dfe7}}
    label{{display:block;margin:12px 0}} input,textarea,select,button{{font:inherit;padding:8px;max-width:95%}}
    textarea{{width:95%;min-height:65px}} button{{background:#174f77;color:white;border:0;border-radius:5px;cursor:pointer}}
    a{{color:#135b8c}} table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;text-align:left;border-bottom:1px solid #ddd}}
    .warn{{color:#9a3600;font-weight:600}}small{{color:#526476}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
    </style><header><small>LOCAL LEARNING PROTOTYPE · v{VERSION} · synthetic data only</small>
    <h1>{html.escape(title)}</h1><a href="/">Enquiries</a></header>{body}</html>'''


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def reply(self, code, data, cookie=None):
        is_json = not isinstance(data, str)
        raw = json.dumps(data).encode() if is_json else data.encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json" if is_json else "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def handle_request(self):
        api = self.path.startswith("/api/")
        try:
            self.route(api)
        except Error as exc:
            self.reply(exc.code, {"error": exc.message} if api else page("Request could not be completed", f'<section>{html.escape(exc.message)}<p><a href="/">Return to enquiries</a></p></section>'))
        except Exception:
            self.reply(500, {"error": "Unexpected error; check the local application"} if api else page("Application error", "<section>Unexpected error.</section>"))

    def route(self, api):
        path = urlparse(self.path).path
        data = {}
        if self.command in ("POST", "PATCH", "DELETE"):
            length = int(self.headers.get("Content-Length", 0))
            if length > 100000:
                raise Error(413, "Request too large")
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw) if "application/json" in self.headers.get("Content-Type", "") else {k: v[0] for k, v in parse_qs(raw.decode(), keep_blank_values=True).items()}
                if not isinstance(data, dict):
                    raise ValueError()
            except (ValueError, UnicodeError):
                raise Error(400, "Invalid request")
        jar = cookies.SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie", ""))
        except cookies.CookieError:
            pass
        sid = jar.get("session")
        session = self.server.sessions.get(sid.value) if sid else None
        if session and session["expires"] < dt.datetime.now().timestamp():
            self.server.sessions.pop(sid.value, None)
            session = None
        if path == "/login" and self.command == "GET":
            return self.reply(200, page("Sign in", '<section><form method="post" action="/login"><label>Account <input name="username" required></label><label>Password <input name="password" type="password" required></label><button>Sign in</button></form></section>'))
        if path in ("/login", "/api/login") and self.command == "POST":
            origin = self.headers.get("Origin")
            if origin and origin != "http://" + self.headers.get("Host", ""):
                raise Error(403, "Cross-origin login denied")
            if not self.server.store.authenticate(data.get("username", ""), data.get("password", "")):
                raise Error(401, "Account or password is incorrect")
            token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            self.server.sessions[token] = {"actor": data["username"], "csrf": csrf, "expires": dt.datetime.now().timestamp() + 28800}
            cookie = f"session={token}; HttpOnly; SameSite=Strict; Path=/"
            return self.reply(200, {"csrf": csrf} if api else page("Signed in", '<section><a href="/">Open enquiries</a></section>'), cookie)
        if not session:
            if not api and self.command == "GET":
                self.send_response(303); self.send_header("Location", "/login"); self.end_headers(); return
            raise Error(401, "Sign in is required")
        actor, csrf = session["actor"], session["csrf"]
        if self.command != "GET":
            supplied = self.headers.get("X-CSRF-Token") if api else data.pop("csrf", "")
            if not supplied or not hmac.compare_digest(supplied, csrf):
                raise Error(403, "Request token is missing or invalid")
        store = self.server.store
        if path in ("/logout", "/api/logout") and self.command == "POST":
            self.server.sessions.pop(sid.value, None)
            return self.reply(200, {"signed_out": True} if api else page("Signed out", '<a href="/login">Sign in</a>'), "session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0")
        if path == "/api/meta" and self.command == "GET":
            return self.reply(200, {"version": VERSION, "today": store.today(), "test_clock": bool(store.test_today), "actor": actor})
        if path in ("/api/enquiries", "/create") and self.command == "POST":
            record = store.create(actor, data)
            return self.reply(201, record if api else page("Enquiry saved", f'<a href="/enquiries/{record["id"]}">Open {record["id"]}</a>'))
        if path == "/api/enquiries" and self.command == "GET":
            return self.reply(200, store.list_records(actor, parse_qs(urlparse(self.path).query).get("ref", [""])[0]))
        parts = path.strip("/").split("/")
        if parts[0] == "api":
            parts = parts[1:]
        if len(parts) >= 2 and parts[0] == "enquiries":
            ref = parts[1]
            if self.command == "GET" and len(parts) in (2, 3):
                record = store.read(actor, ref)
                if len(parts) == 3:
                    if parts[2] not in ("history", "messages"):
                        raise Error(404, "Not found")
                    return self.reply(200, record[parts[2]])
                return self.reply(200, record if api else self.detail(record, actor, csrf))
            if self.command == "POST" and len(parts) == 3:
                if not api and parts[2] == "transfer":
                    data["confirmed"] = data.get("confirmed") == "yes"
                record = store.change(actor, ref, parts[2], data)
                return self.reply(200, record if api else page("Enquiry updated", f'<section><a href="/enquiries/{ref}">Return to {ref}</a></section>'))
            raise Error(405, "History and unsupported operations cannot be changed")
        if path == "/" and self.command == "GET":
            esc = html.escape
            ref = parse_qs(urlparse(self.path).query).get("ref", [""])[0]
            rows = "".join(f'<tr><td><a href="/enquiries/{r["id"]}">{r["id"]}</a></td><td>{esc(r["message"])}</td><td>{r["responsible"]}</td><td>{esc(r["follow_up"])}</td></tr>' for r in store.list_records(actor, ref))
            return self.reply(200, page("Enquiries", f'''<section>Signed in as <strong>{actor}</strong> · Today: {store.today()}
            <form method="post" action="/logout"><input type="hidden" name="csrf" value="{csrf}"><button>Sign out</button></form></section>
            <section><form><label>Find exact reference <input name="ref" value="{esc(ref)}"></label><button>Search</button></form>
            <table><tr><th>Reference</th><th>Enquiry</th><th>Responsible</th><th>Follow-up</th></tr>{rows}</table></section>
            <section><h2>Record an enquiry</h2><form method="post" action="/create"><input type="hidden" name="csrf" value="{csrf}">
            <label>Received time with time zone <input name="received" value="{store.now()}" required></label>
            <label>Resident message <textarea name="message" required></textarea></label>
            <label>Responsible representative <select name="responsible">{self.options(actor)}</select></label>
            <label>Missing information <textarea name="missing"></textarea></label>
            <label>Last action <input name="last_action"></label><label>Next action <input name="next_action"></label>
            <label>Agreed follow-up date <input type="date" name="follow_up" required></label><button>Save enquiry</button></form></section>'''))
        raise Error(404, "Not found")

    def options(self, selected=""):
        return "".join(f'<option value="{name}" {"selected" if name == selected else ""}>{name}</option>' for name in USERS if USERS[name] == "representative")

    def detail(self, r, actor, csrf):
        esc = html.escape
        hidden = f'<input type="hidden" name="csrf" value="{csrf}">'
        base = f'/enquiries/{r["id"]}'
        fields = "".join(f'<label>{label}<textarea name="{key}">{esc(r[key])}</textarea></label>' for key, label in (("address", "Collection address"), ("missing", "Outstanding information"), ("last_action", "Last action"), ("next_action", "Next action")))
        messages = "".join(f'<p><strong>{m["direction"]}</strong> · {esc(m["recorded"])}<br>{esc(m["text"])}</p>' for m in r["messages"])
        history = "".join(f'<tr><td>{e["actor"]}<br>{esc(e["timestamp"])}</td><td>{esc(e["field"])}</td><td><pre>{esc(e["old_value"])}</pre></td><td><pre>{esc(e["new_value"])}</pre>{esc(e["reason"])}</td></tr>' for e in r["history"])
        admin = ""
        if USERS[actor] == "supervisor":
            admin = f'''<section><h2>Supervisor assignments</h2><form method="post" action="{base}/cover">{hidden}
            <label>Cover <select name="representative"><option value="">No cover</option>{self.options(r["cover"])}</select></label><button>Save cover</button></form>
            <h3>Permanent transfer</h3><p>Remove temporary cover first. Confirm the receiving representative can take over.</p>
            <form method="post" action="{base}/transfer">{hidden}<label>New responsible representative <select name="representative">{self.options()}</select></label>
            <label>Reason <input name="reason" required></label><label><input type="checkbox" name="confirmed" value="yes" required> Receiving representative confirmed able to take over</label><button>Transfer responsibility</button></form></section>'''
        return page(r["id"], f'''<section><p>{esc(r["message"])}</p><p>Received: {esc(r["received"])}</p>
        <p>Responsible: <strong>{r["responsible"]}</strong> · Cover: <strong>{r["cover"] or "None"}</strong> · State: {r["state"]}</p>
        <p class="warn">{"Follow-up overdue — staff review required" if r["overdue"] else ""}</p>
        <form method="post" action="{base}/update">{hidden}{fields}<label>Follow-up date <input type="date" name="follow_up" value="{r["follow_up"]}" required></label><button>Save details</button></form></section>
        <section><h2>Correspondence</h2>{messages}<form method="post" action="{base}/message">{hidden}<label>Direction <select name="direction"><option value="incoming">Incoming</option><option value="outgoing">Outgoing — stored only</option></select></label>
        <label>Message <textarea name="text" required></textarea></label><button>Record message</button></form><p><small>No email is sent.</small></p></section>{admin}
        <section><h2>Change history</h2><table><tr><th>Who / when (UTC)</th><th>Changed item</th><th>Previous</th><th>New / reason</th></tr>{history}</table></section>''')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(Path(__file__).parent / "local-data" / "enquiries.sqlite"))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--test-today", help="Isolated test date YYYY-MM-DD; never changes the computer clock")
    args = parser.parse_args()
    if args.test_today:
        dt.date.fromisoformat(args.test_today)
    store = Store(args.db, args.test_today)
    if args.init:
        credentials = store.init_users()
        credential_path = Path(args.db).parent / "credentials.json"
        if credentials:
            credential_path.write_text(json.dumps(credentials, indent=2), encoding="utf-8")
        print(f"Accounts initialised. Local credentials: {credential_path}", flush=True)
        return
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.store, server.sessions = store, {}
    print(f"Enquiry tracking {VERSION}: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
