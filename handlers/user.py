#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib.judgement import *
from lib import db
from lib import encrypt
import json


# user handler
class UserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UserHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        username = self.get_argument('username', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if username:
            user_info = db.get_user(username)
        else:
            user_info = db.get_user(username, start, count)

        if user_info:
            ok = True
            info = user_info
        else:
            ok = False
            info = 'get user info failed'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
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
                user_data['salt'], user_data['passwd'] = encrypt.md5_salt(data['passwd'])
                if db.insert_user(user_data):
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
                    saved_user_data = db.get_user(user_data['username'])
                    saved_salt = saved_user_data['salt']
                    saved_passwd = saved_user_data['passwd']
                    _, encrypt_passwd = encrypt.md5_salt(user_data['old_passwd'], saved_salt)
                    if saved_passwd == encrypt_passwd:
                        user_data['salt'], user_data['passwd'] = encrypt.md5_salt(data['new_passwd'])
                if db.update_user(user_data):
                    ok = True
                    info = 'add user successful'
                else:
                    ok = False
                    info = 'add user failed'
            else:
                ok = False
                info = 'unsupported user action'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        user_id = self.get_argument('user_id')

        if db.delete_user:
            ok = True
            info = 'delete user successful'
        else:
            ok = False
            info = 'delete user failed'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))


# 登陆接口
class UserLoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UserLoginHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):


        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            ok = False
            info = 'body or content-type format error'
        else:
            user_info = json.loads(body)
            username = user_info['username']
            password = user_info['passwd']
            saved_user_data = db.get_user(username)
            saved_salt = saved_user_data['salt']
            saved_passwd = saved_user_data['passwd']
            _, encrypt_passwd =  encrypt.md5_salt(password, saved_salt)
            if saved_passwd == encrypt_passwd:
                access_token = encrypt.make_cookie_secret()
                ok = True
                info = {'access_token': access_token}
            else:
                ok = False
                info = 'username or password error'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/admin/user', UserHandler),
    ('/admin/user_login', UserLoginHandler),
]