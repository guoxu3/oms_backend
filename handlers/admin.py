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

    def get(self):
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

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        username = self.get_argument('username')
        if db_user.delete(username):
            ok = True
            info = 'delete user successful'
        else:
            ok = False
            info = 'delete user failed'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


# 登陆接口
class UserLoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UserLoginHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

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
            # 根据用户名获取存在数据库中的salt值和加密字符串，与传入的密码加密后的值进行比对
            saved_user_data = db_user.get(username)
            saved_salt = saved_user_data['salt']
            saved_passwd = saved_user_data['passwd']
            _, encrypt_passwd = encrypt.md5_salt(password, saved_salt)
            if saved_passwd == encrypt_passwd:
                # 生成session信息并写到数据库中
                access_token = encrypt.make_cookie_secret()
                session_data = {'access_token': access_token, 'username': username, 'create_time': cur_timestamp()}
                session_data['expire_time'] = session_data['create_time'] + config.expire_second
                if db_session.update(session_data):
                    self.set_secure_cookie("access_token", access_token, domain=".miaodeli.com", path="/")
                    ok = True
                    info = {}
                else:
                    ok = False
                    info = "error ,please contact with the system administrator"
            else:
                ok = False
                info = 'username or password error'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


# permission handler
class PermissionHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(PermissionHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    def get(self):
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        permission_info = db_permission.get(start, count)
        if permission_info:
            ok = True
            info = {'data': permission_info, 'count': db_permission.row_count()}
        else:
            ok = False
            info = 'get permission info failed'

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
                # todo
                ok = ''
                info = ''
            else:
                ok = False
                info = 'unsupported permission action'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/user', UserHandler),
    ('/api/user_login', UserLoginHandler),
    ('/api/permission', PermissionHandler),
]