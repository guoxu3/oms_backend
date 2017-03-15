#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib import verify, encrypt, mail
from db import db_utils
import check


class TaskStatisticHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskStatisticHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.token = self.get_secure_cookie("access_token")
        self.handler_permission = '7'
        self.get_permission = '7.1'
        self.post_permission = '7.2'
        self.delete_permission = '7.3'

    def get(self):
        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.get_permission]
        ok, info, _ = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        username = self.get_argument('username', None)
        begin_time = int(self.get_argument('begin_time', 1483200000))
        end_time = int(self.get_argument('end_time', 4102415999))
        is_all = self.get_argument('is_all', False)
        if is_all:
            task_statistic_info = db_utils.get_all_user_task_statistic_by_time(begin_time, end_time)
        else:
            task_statistic_info = db_utils.get_task_statistic_by_time(begin_time, end_time, username)

        if task_statistic_info != False:
            ok = True
            info = {'data': task_statistic_info}
        else:
            ok = False
            info = 'Get task statistic info failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/task_statistic', TaskStatisticHandler),
]
