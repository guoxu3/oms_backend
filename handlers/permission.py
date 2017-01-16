#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from models.db import db_user,db_permission,db_session
from lib import encrypt
from lib import config
import json


# permission handler
class PermissionHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(PermissionHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.handler_permission = '3'
        self.get_permission = '3.1'
        self.post_permission = '3.2'
        self.delete_permission = '3.3'
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
                start = self.get_argument('start', 0)
                count = self.get_argument('count', 10)
                permission_info = db_permission.get(start, count)
                if permission_info:
                    ok = True
                    info = {'data': permission_info, 'count': db_permission.row_count()}
                else:
                    ok = False
                    info = 'get permission info failed'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        post_add_permission = '3.2.1'
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
                    local_permission_list = [self.handler_permission, self.get_permission, post_add_permission]
                    if has_permission(self.token, local_permission_list):
                        # todo
                        ok = ''
                        info = ''
                    else:
                        ok = False
                        info = 'no permission'
                else:
                    ok = False
                    info = 'unsupported permission action'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


handlers = [
    ('/api/permission', PermissionHandler),
]