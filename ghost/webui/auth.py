# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import hashlib
import hmac
import os
import secrets
import time

from .db import execute, query_one, now_ts

PBKDF2_ITER = 200000
TOKEN_TTL = int(os.environ.get("GHOST_UI_TOKEN_TTL", "86400"))


def _b64e(data):
    return base64.b64encode(data).decode("ascii")


def _b64d(data):
    return base64.b64decode(data.encode("ascii"))


def hash_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITER)
    return _b64e(salt) + ":" + _b64e(dk)


def verify_password(password, stored):
    try:
        salt_b64, hash_b64 = stored.split(":", 1)
        salt = _b64d(salt_b64)
        expected = _b64d(hash_b64)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITER)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def create_session(user_id):
    token = secrets.token_urlsafe(32)
    created = now_ts()
    expires = created + TOKEN_TTL
    execute(
        "INSERT INTO sessions(token, user_id, created_at, expires_at) VALUES(?, ?, ?, ?)",
        [token, user_id, created, expires],
    )
    return token, expires


def revoke_session(token):
    execute("DELETE FROM sessions WHERE token = ?", [token])


def get_session(token):
    now = now_ts()
    return query_one(
        "SELECT s.token, s.user_id, s.expires_at, u.email, u.role, u.is_active "
        "FROM sessions s JOIN users u ON u.id = s.user_id "
        "WHERE s.token = ? AND s.expires_at > ?",
        [token, now],
    )


def get_user_by_email(email):
    return query_one(
        "SELECT id, email, password_hash, role, is_active, created_at, updated_at "
        "FROM users WHERE email = ?",
        [email],
    )


def get_user_by_id(user_id):
    return query_one(
        "SELECT id, email, role, is_active, created_at, updated_at "
        "FROM users WHERE id = ?",
        [user_id],
    )


def create_user(email, password, role):
    ts = now_ts()
    execute(
        "INSERT INTO users(email, password_hash, role, is_active, created_at, updated_at) "
        "VALUES(?, ?, ?, 1, ?, ?)",
        [email, hash_password(password), role, ts, ts],
    )


def set_user_password(user_id, password):
    ts = now_ts()
    execute(
        "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
        [hash_password(password), ts, user_id],
    )


def set_user_role(user_id, role):
    ts = now_ts()
    execute(
        "UPDATE users SET role = ?, updated_at = ? WHERE id = ?",
        [role, ts, user_id],
    )


def set_user_active(user_id, active):
    ts = now_ts()
    execute(
        "UPDATE users SET is_active = ?, updated_at = ? WHERE id = ?",
        [1 if active else 0, ts, user_id],
    )


def ensure_admin(email, password):
    user = get_user_by_email(email)
    if user:
        return
    create_user(email, password, "admin")
