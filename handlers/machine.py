#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    machine handlers
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


class MachineHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(MachineHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.handler_permission = '6'
        self.get_permission = '6.1'
        self.post_permission = '6.2'
        self.delete_permission = '6.3'
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
                machine_name = self.get_argument('machine_name', None)
                start = self.get_argument('start', 0)
                count = self.get_argument('count', 10)
                if machine_name:
                    machine_info = db_machine.get(machine_name)
                else:
                    machine_info = db_machine.get(machine_name, start, count)

                if machine_info:
                    ok = True
                    info = {'data': machine_info, 'count': db_machine.row_count()}
                else:
                    ok = False
                    info = 'no such a machine info'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        post_add_permission = '6.2.1'
        post_update_permission = '6.2.2'
        if self.ok:
            content_type = dict(self.request.headers)['Content-Type']
            body = self.request.body
            if not is_content_type_right(content_type) or not is_json(body):
                ok = False
                info = 'body or content-type format error'
            else:
                body = json.loads(body)
                action, data = body['action'], body['data']
                if action == 'add':
                    local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
                    if has_permission(self.token, local_permission_list):
                        machine_info_data = data
                        if db_machine.add(machine_info_data):
                            ok = True
                            info = 'add machine info successful'
                        else:
                            ok = False
                            info = 'add miachine info failed'
                    else:
                        ok = False
                        info = 'no permission'
                elif action == 'update':
                    local_permission_list = [self.handler_permission, self.post_permission, post_update_permission]
                    if has_permission(self.token, local_permission_list):
                        machine_info_data = data
                        if db_machine.add(machine_info_data):
                            ok = True
                            info = 'update task status successful'
                        else:
                            ok = False
                            info = 'update task status failed'
                    else:
                        ok = False
                        info = 'no permission'
                else:
                    ok = False
                    info = 'unsupported task status action'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        local_permission_list = [self.handler_permission, self.delete_permission]
        if self.ok:
            if has_permission(self.token, local_permission_list):
                machine_name = self.get_argument('machine_name')
                if db_machine.delete(machine_name):
                    ok = True
                    info = 'delete task successful'
                else:
                    ok = False
                    info = 'delete task  failed'
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
    ('/api/machine', MachineHandler),
]
