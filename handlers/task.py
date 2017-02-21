#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    task handlers
"""

import tornado.web
import tornado.escape
from lib import verify, common, encrypt, mail
from models.db import db_task
import uuid
import json
import public


class TaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.token = self.get_secure_cookie("access_token")
        self.handler_permission = '1'
        self.get_permission = '1.1'
        self.post_permission = '1.2'
        self.delete_permission = '1.3'

    def get(self):
        ok, info = public.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.get_permission]
        ok, info = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        task_info = db_task.get(task_id, start, count)
        if task_info:
            ok = True
            info = {'data': task_info, 'count': db_task.row_count()}
        else:
            ok = False
            info = 'No such a task'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_add_permission = '1.2.1'

        ok, info = public.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = public.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, task_data, mailto = body['action'], body['data'], body['mailto']
        print action, task_data, mailto
        if action == 'add':
            local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
            ok, info = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            task_data['task_id'] = uuid.uuid1().hex
            task_data['create_time'] = common.cur_timestamp()
            if db_task.add(task_data):
                if list(mailto):
                    message = task_data['creator'] + " create a new task, see in " \
                                                     "http://oms.example.com/task?task_id=" + task_data['task_id']
                    mail.send_mail(list(mailto), message)
                ok = True
                info = {'task_id': task_data['task_id']}
            else:
                ok = False
                info = 'Add task failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported task action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def delete(self):
        ok, info = public.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.delete_permission]
        ok, info = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        task_id = self.get_argument('task_id')
        if db_task.get(task_id):
            if db_task.delete(task_id):
                ok = True
                info = 'Delete task successful'
            else:
                ok = False
                info = 'Delete task failed'
        else:
            ok = True
            info = 'No such a task'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/task', TaskHandler),
]
