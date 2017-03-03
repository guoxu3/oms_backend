#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    user handler
"""

import tornado.web
import tornado.escape
from lib import verify, encrypt, mail
from db import db_user,db_permission,db_session
import json
import check


class UserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UserHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.handler_permission = '4'
        self.get_permission = '4.1'
        self.post_permission = '4.2'
        self.delete_permission = '4.3'
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

        username = self.get_argument('username', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)

        user_info = db_user.get(username, start, count)
        if user_info:
            ok = True
            info = {'data': user_info, 'count': db_user.row_count()}
        else:
            ok = False
            info = 'Get user info failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_add_permission = '4.2.1'
        post_user_update_permission = '4.2.2'
        post_admin_update_permission = '4.2.3'

        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = check.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, user_data = body['action'], body['data']
        if action == 'add':
            local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            user_data['salt'], user_data['passwd'] = encrypt.md5_salt(user_data['passwd'])
            if db_user.add(user_data):
                ok = True
                info = 'Add user successful'
            else:
                ok = False
                info = 'Add user failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if action == 'update':
            local_permission_list = [self.handler_permission, self.post_permission, post_user_update_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            ok, info = check.check_user_input(user_data)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            if 'old_passwd' in user_data:
                ok, info = check.check_password(user_data['username'], user_data['old_passwd'])
                if not ok:
                    self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                    return

                user_data['salt'], user_data['passwd'] = encrypt.md5_salt(user_data['new_passwd'])

            if db_user.update(user_data):
                ok = True
                info = 'Update password successful'
            else:
                ok = False
                info = 'Update password failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        # update user info without verify password
        if action == 'update_all':
            local_permission_list = [self.handler_permission, self.post_permission, post_admin_update_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            ok, info = check.check_user_input(user_data)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            user_data['salt'], user_data['passwd'] = encrypt.md5_salt(user_data['passwd'])
            if db_user.update(user_data):
                ok = True
                info = 'Update user info successful'
            else:
                ok = False
                info = 'Update user info failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported user action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def delete(self):
        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.delete_permission]
        ok, info, is_admin = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if not is_admin:
            ok = False
            info = "Only admin can delete a user"
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        username = self.get_argument('username')
        if db_user.delete(username):
            ok = True
            info = 'Delete user successful'
        else:
            ok = False
            info = 'Delete user failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass

handlers = [
    ('/api/user', UserHandler),
]
