# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

from .db import execute, query_one, now_ts


class TaskRunner(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.queue = Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._worker)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._stop.set()

    def submit(self, task_id):
        self.queue.put(task_id)

    def requeue_pending(self):
        rows = execute(
            "SELECT id FROM tasks WHERE status IN ('queued','running')"
        ).fetchall()
        for row in rows:
            self.submit(row["id"])

    def _worker(self):
        while not self._stop.is_set():
            try:
                task_id = self.queue.get(timeout=1)
            except Empty:
                continue
            self._process(task_id)
            self.queue.task_done()

    def _process(self, task_id):
        task = query_one("SELECT * FROM tasks WHERE id = ?", [task_id])
        if not task:
            return
        execute(
            "UPDATE tasks SET status = ?, started_at = ? WHERE id = ?",
            ["running", now_ts(), task_id],
        )
        allow_shell = bool(task["payload"]) and task["payload"] == "allow_shell"
        output, error = self.runtime.run_command(
            task["command"] or "", allow_shell=allow_shell
        )
        status = "success" if not error else "failed"
        execute(
            "UPDATE tasks SET status = ?, finished_at = ?, output = ?, error = ? WHERE id = ?",
            [status, now_ts(), output, error, task_id],
        )
        time.sleep(0.05)
