# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import time
import json
import shutil

from . import auth
from .db import query_one, query_all, now_ts
from .handlers_core import BaseHandler, audit_log


def tail_file(path, lines=200):
    if not os.path.isfile(path):
        return ""
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        end = f.tell()
        data = b""
        while end > 0 and data.count(b"\n") <= lines:
            size = min(4096, end)
            end -= size
            f.seek(end)
            data = f.read(size) + data
        return data.decode("utf-8", "ignore")


class ConfigHandler(BaseHandler):
    def get(self):
        self.require_user()
        path = self.runtime.config.user_path
        if not os.path.isfile(path):
            _ = self.runtime.config
        with open(path, "r") as f:
            content = f.read()
        self.write_json({"path": path, "content": content})

    def post(self):
        self.require_admin()
        data = self.read_json()
        content = data.get("content")
        if content is None:
            self.write_json({"error": "content required"}, status=400)
            return
        path = self.runtime.config.user_path
        backup_dir = os.path.join(self.data_dir, "config-backups")
        if not os.path.isdir(backup_dir):
            os.makedirs(backup_dir)
        ts = time.strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(backup_dir, "ghost.conf." + ts)
        if os.path.isfile(path):
            shutil.copyfile(path, backup_path)
        with open(path, "w") as f:
            f.write(content)
        audit_log(self.current_user["user_id"], "config_update", path, backup_path, self.request.remote_ip)
        self.write_json({"ok": True, "backup": backup_path})


class UsersHandler(BaseHandler):
    def get(self):
        self.require_admin()
        rows = query_all("SELECT id, email, role, is_active, created_at FROM users ORDER BY id ASC")
        self.write_json({"users": [dict(r) for r in rows]})

    def post(self):
        self.require_admin()
        data = self.read_json()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        role = (data.get("role") or "user").strip()
        if not email or not password:
            self.write_json({"error": "email and password required"}, status=400)
            return
        if role not in ("admin", "user"):
            self.write_json({"error": "invalid role"}, status=400)
            return
        if auth.get_user_by_email(email):
            self.write_json({"error": "email already exists"}, status=409)
            return
        auth.create_user(email, password, role)
        audit_log(self.current_user["user_id"], "user_create", email, role, self.request.remote_ip)
        self.write_json({"ok": True})


class UserDetailHandler(BaseHandler):
    def patch(self, user_id):
        self.require_admin()
        data = self.read_json()
        if "password" in data and data["password"]:
            auth.set_user_password(user_id, data["password"])
        if "role" in data and data["role"] in ("admin", "user"):
            auth.set_user_role(user_id, data["role"])
        if "is_active" in data:
            auth.set_user_active(user_id, bool(data["is_active"]))
        audit_log(self.current_user["user_id"], "user_update", str(user_id), json.dumps(data), self.request.remote_ip)
        user = auth.get_user_by_id(user_id)
        if not user:
            self.write_json({"error": "not found"}, status=404)
            return
        self.write_json({"user": dict(user)})


class AuditHandler(BaseHandler):
    def get(self):
        self.require_admin()
        limit = int(self.get_argument("limit", "100"))
        rows = query_all("SELECT * FROM audit ORDER BY id DESC LIMIT ?", [limit])
        self.write_json({"audit": [dict(r) for r in rows]})


class LogsHandler(BaseHandler):
    def get(self):
        self.require_admin()
        lines = int(self.get_argument("lines", "200"))
        content = tail_file(self.log_path, lines=lines)
        self.write_json({"path": self.log_path, "content": content})
