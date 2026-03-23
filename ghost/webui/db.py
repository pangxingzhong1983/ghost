# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sqlite3
import threading
import time

DB_PATH = os.environ.get("GHOST_UI_DB", "/data/ghostui.db")

_local = threading.local()


def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_conn():
    if not hasattr(_local, "conn"):
        _local.conn = _connect()
    return _local.conn


def now_ts():
    return int(time.time())


def init_db():
    conn = get_conn()
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=NORMAL;

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            expires_at INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            command TEXT,
            payload TEXT,
            status TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            started_at INTEGER,
            finished_at INTEGER,
            output TEXT,
            error TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            target TEXT,
            detail TEXT,
            ip TEXT,
            created_at INTEGER NOT NULL
        );
        """
    )
    conn.commit()


def execute(sql, params=None):
    conn = get_conn()
    cur = conn.execute(sql, params or [])
    conn.commit()
    return cur


def query_one(sql, params=None):
    cur = get_conn().execute(sql, params or [])
    return cur.fetchone()


def query_all(sql, params=None):
    cur = get_conn().execute(sql, params or [])
    return cur.fetchall()
