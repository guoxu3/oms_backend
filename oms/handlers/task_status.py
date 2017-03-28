#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
update task status handlers
"""

import tornado.web
import tornado.escape
from db import db_task, db_machine
import json
import check


# 调用更新脚本
class TaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskStatusHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.token = self.get_secure_cookie("access_token")

    def post(self):
        ok, info = check.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        task_status = json.loads(self.request.body)
        if not db_task.update(task_status):
            ok = False
            info = 'update task status failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = True
        info = "info = 'update task status successful"
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/task_status', TaskStatusHandler),
]
