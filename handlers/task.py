#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    task handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from lib.encrypt import *
from lib.send_mail import send_mail
from models.db import db_task,db_task_status,db_machine
import uuid
import json


class TaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.handler_permission = '1'
        self.get_permission = '1.1'
        self.post_permission = '1.2'
        self.delete_permission = '1.3'
        self.ok = True
        self.info = ""
        self.token = self.get_secure_cookie("access_token")
        if self.token:
            if is_expired(self.token):
                self.ok = False
                self.info = "login time out"
        else:
            self.ok = False
            self.info = "please login first"

    def get(self):
        local_permission_list = [self.handler_permission,self.get_permission]
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if self.ok:
            if has_permission(self.token, local_permission_list):
                task_info = db_task.get(task_id, start, count)
                if task_info:
                    ok = True
                    info = {'data': task_info, 'count': db_task.row_count()}
                else:
                    ok = False
                    info = 'no such a task'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        post_add_permission = '1.2.1'
        if self.ok:
            content_type = dict(self.request.headers)['Content-Type']
            body = self.request.body
            if not is_content_type_right(content_type) or not is_json(body):
                ok = False
                info = 'body or content-type format error'
            else:
                body = json.loads(body)
                action, task_data, mailto = body['action'], body['data'], body['mailto']
                if action == 'add':
                    local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
                    if has_permission(self.token, local_permission_list):
                        task_data['task_id'] = uuid.uuid1().hex
                        task_data['create_time'] = cur_timestamp()
                        if db_task.add(task_data):
                            if list(mailto):
                                message = task_data['creator'] + " create a new task, see in " \
                                                        "http://oms.example.com/task?task_id=" + task_data['task_id']
                                send_mail(list(mailto), message)
                            ok = True
                            info = {'task_id': task_data['task_id']}
                        else:
                            ok = False
                            info = 'add task failed'
                    else:
                        ok = False
                        info = 'no permission'
                else:
                    ok = False
                    info = 'unsupported task action'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        local_permission_list = [self.handler_permission, self.delete_permission]
        if self.ok:
            if has_permission(self.token, local_permission_list):
                task_id = self.get_argument('task_id')
                if db_task.get(task_id):
                    if db_task.delete(task_id):
                        ok = True
                        info = 'delete task successful'
                    else:
                        ok = False
                        info = 'delete task failed'
                else:
                    ok = False
                    info = 'no such a task'
            else:
                    ok = False
                    info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/task', TaskHandler),
]
