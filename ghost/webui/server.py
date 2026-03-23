# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

import tornado.ioloop
import tornado.web

from .db import init_db
from .auth import ensure_admin
from .runtime import GhostRuntime
from .tasks import TaskRunner
from .handlers_core import (
    HealthHandler, LoginHandler, LogoutHandler, MeHandler,
    TasksHandler, TaskDetailHandler, IndexHandler,
)
from .handlers_admin import (
    ConfigHandler, UsersHandler, UserDetailHandler,
    AuditHandler, LogsHandler,
)
from .terminal import TerminalWebSocket


def setup_logging(data_dir):
    log_dir = os.path.join(data_dir, "logs")
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    log_path = os.path.join(log_dir, "webui.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s|%(levelname)s|%(name)s|%(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    return log_path


def make_app(runtime, runner, data_dir, log_path):
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return tornado.web.Application(
        [
            (r"/api/health", HealthHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/login", LoginHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/logout", LogoutHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/me", MeHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/tasks", TasksHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/tasks/([0-9]+)", TaskDetailHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/config", ConfigHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/users", UsersHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/users/([0-9]+)", UserDetailHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/audit", AuditHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/api/logs", LogsHandler, dict(runtime=runtime, runner=runner, data_dir=data_dir, log_path=log_path)),
            (r"/ws/terminal", TerminalWebSocket, dict(data_dir=data_dir)),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/(.*)", IndexHandler, dict(static_path=static_path)),
        ],
        debug=False,
    )


def main():
    data_dir = os.environ.get("GHOST_UI_DATA", "/data")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    log_path = setup_logging(data_dir)
    init_db()
    admin_email = os.environ.get("GHOST_UI_ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("GHOST_UI_ADMIN_PASSWORD", "admin123")
    ensure_admin(admin_email, admin_password)
    runtime = GhostRuntime()
    runner = TaskRunner(runtime)
    runner.requeue_pending()
    host = os.environ.get("GHOST_UI_HOST", "0.0.0.0")
    port = int(os.environ.get("GHOST_UI_PORT", "8089"))
    app = make_app(runtime, runner, data_dir, log_path)
    app.listen(port, address=host)
    logging.info("ghost web ui started on %s:%s", host, port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
