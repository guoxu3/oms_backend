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

    def get(self):
        username = self.get_argument('username')
        user_info = db.get_user(username)
        if user_info:
            code = 200
            info = user_info
        else:
            code = 500
            info = 'get user info failed'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                user_data = data
                user_data['salt'], user_data['passwd'] = encrypt.md5_salt(data['passwd'])
                if db.insert_user(user_data):
                    code = 200
                    info = 'add user successful'
                else:
                    code = 500
                    info = 'add user failed'
            elif action == 'update':
                user_data = data
                if db.update_user(user_data):
                    code = 200
                    info = 'add user successful'
                else:
                    code = 500
                    info = 'add user failed'
            else:
                code = 400
                info = 'unsupported user action'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        user_id = self.get_argument('user_id')

        if db.delete_user:
            code = 200
            info = 'delete user successful'
        else:
            code = 500
            info = 'delete user failed'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))


# 登陆接口
class UserLoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            info = 'body or content-type format error'
        else:
            user_info = json.loads(body)
            username = user_info['username']
            password = user_info['passwd']
            saved_user_data = db.get_user(username)
            saved_salt = saved_user_data['salt']
            print saved_user_data
            saved_passwd = saved_user_data['passwd']
            _, encrypt_passwd =  encrypt.md5_salt(password, saved_salt)
            if saved_passwd == encrypt_passwd:
                access_token = encrypt.make_cookie_secret()
                code = 200
                info = {'access_token': access_token}
            else:
                code = 400
                info = 'username or password error'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/admin/user', UserHandler),
    ('/admin/user_login', UserLoginHandler),
]