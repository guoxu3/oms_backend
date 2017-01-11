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


# user handler
class UserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UserHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
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
        if self.ok:
            if has_permission(self.token, local_permission):
                username = self.get_argument('username', None)
                start = self.get_argument('start', 0)
                count = self.get_argument('count', 10)
                if username:
                    user_info = db_user.get(username)
                else:
                    user_info = db_user.get(username, start, count)

                if user_info:
                    ok = True
                    info = {'data': user_info, 'count': db_user.row_count()}
                else:
                    ok = False
                    info = 'get user info failed'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        if self.ok:
            if has_permission(self.token, local_permission):
                content_type = dict(self.request.headers)['Content-Type']
                body = self.request.body
                if not is_content_type_right(content_type) or not is_json(body):
                    ok = False
                    info = 'body or content-type format error'
                else:
                    body = json.loads(body)
                    action, data = body['action'], body['data']
                    if action == 'add':
                        user_data = data
                        print data
                        user_data['salt'], user_data['passwd'] = encrypt.md5_salt(data['passwd'])
                        if db_user.add(user_data):
                            ok = True
                            info = 'add user successful'
                        else:
                            ok = False
                            info = 'add user failed'
                    elif action == 'update':
                        user_data = data
                        # 改密码,确认有新旧密码数据
                        if user_data.has_key('old_passwd') and user_data.has_key('new_passwd'):
                            # 判断旧密码是否正确
                            saved_user_data = db_user.get(user_data['username'])
                            saved_salt = saved_user_data['salt']
                            saved_passwd = saved_user_data['passwd']
                            _, encrypt_passwd = encrypt.md5_salt(user_data['old_passwd'], saved_salt)
                            if saved_passwd == encrypt_passwd:
                                user_data['salt'], user_data['passwd'] = encrypt.md5_salt(data['new_passwd'])
                                if db_user.update(user_data):
                                    ok = True
                                    info = 'update user successful'
                                else:
                                    ok = False
                                    info = 'update user failed'
                            else:
                                ok = False
                                info = 'password auth failed'
                        else:
                            if db_user.update(user_data):
                                ok = True
                                info = 'update user successful'
                            else:
                                ok = False
                                info = 'update user failed'
                    else:
                        ok = False
                        info = 'unsupported user action'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        if self.ok:
            if has_permission(self.token, local_permission):
                username = self.get_argument('username')
                if db_user.delete(username):
                    ok = True
                    info = 'delete user successful'
                else:
                    ok = False
                    info = 'delete user failed'
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
    ('/api/user', UserHandler),
]