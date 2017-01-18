#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    task status handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from lib.encrypt import *
from models.salt_api import SaltAPI as sapi
from models.db import db_task,db_task_status,db_machine
import uuid
import json


class TaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskStatusHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.handler_permission = 2
        self.get_permission = 2.1
        self.post_permision = 2.2
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
        local_permission_list = [self.handler_permission, self.get_permission]
        if self.ok:
            if has_permission(self.token, local_permission_list):
                task_id = self.get_argument('task_id', None)
                start = self.get_argument('start', 0)
                count = self.get_argument('count', 10)
                if task_id:
                    task_status_info = db_task_status.get(task_id)
                else:
                    task_status_info = db_task_status.get(task_id, start, count)

                if task_status_info:
                    ok = True
                    info = {'data': task_status_info, 'count': db_task_status.row_count()}
                else:
                    ok = False
                    info = 'no such a task status'
            else:
                    ok = False
                    info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        """
        update task status, called by shell script
        Does not require authentication
        """
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            ok = False
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'update':
                task_status_data = data
                if db_task_status.update(task_status_data):
                    ok = True
                    info = 'update task status successful'
                else:
                    ok = False
                    info = 'update task status failed'
            else:
                ok = False
                info = 'unsupported task status action'


        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/task_status', TaskStatusHandler),
]
