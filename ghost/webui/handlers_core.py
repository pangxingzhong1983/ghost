# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import tornado.web
import tornado.escape

from . import auth
from .db import execute, query_one, query_all, now_ts


def audit_log(user_id, action, target=None, detail=None, ip=None):
    execute(
        "INSERT INTO audit(user_id, action, target, detail, ip, created_at) "
        "VALUES(?, ?, ?, ?, ?, ?)",
        [user_id, action, target, detail, ip, now_ts()],
    )


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, runtime=None, runner=None, data_dir=None, log_path=None):
        self.runtime = runtime
        self.runner = runner
        self.data_dir = data_dir
        self.log_path = log_path

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")

    def _get_token(self):
        token = ""
        auth_header = self.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        if not token:
            token = self.request.headers.get("X-Token", "")
        if not token:
            token = self.get_cookie("token", "")
        return token

    def get_current_user(self):
        token = self._get_token()
        if not token:
            return None
        session = auth.get_session(token)
        if not session or not session["is_active"]:
            return None
        return session

    def require_user(self):
        if not self.current_user:
            raise tornado.web.HTTPError(401)

    def require_admin(self):
        self.require_user()
        if self.current_user["role"] != "admin":
            raise tornado.web.HTTPError(403)

    def read_json(self):
        if not self.request.body:
            return {}
        return tornado.escape.json_decode(self.request.body)

    def write_json(self, data, status=200):
        self.set_status(status)
        self.finish(tornado.escape.json_encode(data))


class HealthHandler(BaseHandler):
    def get(self):
        self.write_json({"ok": True, "ts": now_ts()})


class LoginHandler(BaseHandler):
    def post(self):
        data = self.read_json()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        if not email or not password:
            self.write_json({"error": "missing credentials"}, status=400)
            return
        user = auth.get_user_by_email(email)
        if not user or not auth.verify_password(password, user["password_hash"]):
            audit_log(None, "login_failed", email, None, self.request.remote_ip)
            self.write_json({"error": "invalid credentials"}, status=401)
            return
        if not user["is_active"]:
            self.write_json({"error": "account disabled"}, status=403)
            return
        token, expires = auth.create_session(user["id"])
        self.set_cookie("token", token, httponly=True, samesite="Strict")
        audit_log(user["id"], "login", email, None, self.request.remote_ip)
        self.write_json({
            "token": token,
            "expires_at": expires,
            "user": {"id": user["id"], "email": user["email"], "role": user["role"]},
        })


class LogoutHandler(BaseHandler):
    def post(self):
        token = self._get_token()
        session = auth.get_session(token) if token else None
        if token:
            auth.revoke_session(token)
        self.clear_cookie("token")
        if session:
            audit_log(session["user_id"], "logout", None, None, self.request.remote_ip)
        self.write_json({"ok": True})


class MeHandler(BaseHandler):
    def get(self):
        self.require_user()
        self.write_json({
            "user": {
                "id": self.current_user["user_id"],
                "email": self.current_user["email"],
                "role": self.current_user["role"],
            }
        })


class TasksHandler(BaseHandler):
    def get(self):
        self.require_user()
        limit = int(self.get_argument("limit", "50"))
        offset = int(self.get_argument("offset", "0"))
        rows = query_all(
            "SELECT * FROM tasks ORDER BY id DESC LIMIT ? OFFSET ?",
            [limit, offset],
        )
        self.write_json({"tasks": [dict(r) for r in rows]})

    def post(self):
        self.require_user()
        data = self.read_json()
        cmd = (data.get("command") or "").strip()
        if not cmd:
            self.write_json({"error": "command required"}, status=400)
            return
        allow_shell = cmd.startswith("!")
        if allow_shell and self.current_user["role"] != "admin":
            self.write_json({"error": "shell command requires admin"}, status=403)
            return
        payload = "allow_shell" if allow_shell else ""
        cur = execute(
            "INSERT INTO tasks(user_id, type, command, payload, status, created_at) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            [self.current_user["user_id"], "command", cmd, payload, "queued", now_ts()],
        )
        task_id = cur.lastrowid
        self.runner.submit(task_id)
        audit_log(self.current_user["user_id"], "task_create", cmd, None, self.request.remote_ip)
        task = query_one("SELECT * FROM tasks WHERE id = ?", [task_id])
        self.write_json({"task": dict(task)})


class TaskDetailHandler(BaseHandler):
    def get(self, task_id):
        self.require_user()
        task = query_one("SELECT * FROM tasks WHERE id = ?", [task_id])
        if not task:
            self.write_json({"error": "not found"}, status=404)
            return
        self.write_json({"task": dict(task)})


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, static_path=None):
        self.static_path = static_path

    def set_default_headers(self):
        self.set_header("Content-Type", "text/html; charset=utf-8")

    def get(self, _path=""):
        index_path = os.path.join(self.static_path, "index.html")
        with open(index_path, "r") as f:
            self.finish(f.read())
