#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    machine handlers
"""

import tornado.web
import tornado.escape
from lib import verify, common, encrypt
from models.db import db_task, db_machine
import public
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
        self.token = self.get_secure_cookie("access_token")

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

        machine_name = self.get_argument('machine_name', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)

        machine_info = db_machine.get(machine_name, start, count)
        if machine_info:
            ok = True
            info = {'data': machine_info, 'count': db_machine.row_count()}
        else:
            ok = False
            info = 'No such a machine info'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_add_permission = '6.2.1'
        post_update_permission = '6.2.2'

        ok, info = public.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = public.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, data = body['action'], body['data']
        if action == 'add':
            local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
            ok, info = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            machine_info_data = data
            if db_machine.add(machine_info_data):
                ok = True
                info = 'Add machine info successful'
            else:
                ok = False
                info = 'Add miachine info failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if action == 'update':
            local_permission_list = [self.handler_permission, self.post_permission, post_update_permission]
            ok, info = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            machine_info_data = data
            if db_machine.add(machine_info_data):
                ok = True
                info = 'update task status successful'
            else:
                ok = False
                info = 'update task status failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported task status action'
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

        machine_name = self.get_argument('machine_name')
        if db_machine.delete(machine_name):
            ok = True
            info = 'Delete task successful'
        else:
            ok = False
            info = 'Delete task  failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/machine', MachineHandler),
]
