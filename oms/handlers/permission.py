#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib import verify, encrypt, mail
from db import db_user,db_permission,db_session
import check
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
        self.token = self.get_secure_cookie("access_token")

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

        start = int(self.get_argument('start', 0))
        count = int(self.get_argument('count', 10))
        permission = self.get_argument('permission', None)
        is_all = self.get_argument('all', False)
        permission_info = db_permission.get(is_all, start, count, permission)
        if permission_info:
            ok = True
            info = {'data': permission_info, 'count': db_permission.row_count()}
        else:
            ok = False
            info = 'Get permission info failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_add_permission = '3.2.1'
        post_update_permission = '3.2.2'

        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = check.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, permission_data = body['action'], body['data']
        if action == 'add':
            local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            if db_permission.add(permission_data):
                ok = True
                info = 'Add permission successful'
            else:
                ok = False
                info = 'Add permission failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if action == 'update':
            local_permission_list = [self.handler_permission, self.post_permission, post_update_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            if db_permission.update(permission_data):
                ok = True
                info = 'Update permission successful'
            else:
                ok = False
                info = 'Update permission failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported permission action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def delete(self):
        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.delete_permission]
        ok, info, _ = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        permission = self.get_argument('permission')
        permission_data = db_permission.get(permission)
        if not permission_data:
            ok = True
            info = 'No such a permission info'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if db_permission.delete(permission):
            ok = True
            info = 'Delete permission info successful'
        else:
            ok = False
            info = 'Delete permission info  failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass

handlers = [
    ('/api/permission', PermissionHandler),
]
