#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib.judgement import *
from lib import db
import uuid
import json
import time


# 新增用户
class AddUserHnadler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            user_info = json.loads(body)
            if db.insert_user(user_info):
                code = 200
                data = {}
                message = 'add user successful'
            else:
                code = 500
                data = {}
                message = 'add user failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 更新用户信息
class UpdateUserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            user_info = json.loads(body)
            if db.update_user(user_info):
                code = 200
                data = {}
                message = 'update user successful'
            else:
                code = 500
                data = {}
                message = 'update user failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 获取用户信息
class GetUserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        mail = self.get_argument('mail')
        task_info = db.get_user(mail)
        if task_info:
            code = 200
            data = task_info
            message = 'get user successful'
        else:
            code = 500
            data = {}
            message = 'no such a user'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 删除用户
class DeleteUserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            mail = json.loads(body)['mail']
            if db.delete_task(mail):
                code = 200
                data = {}
                message = 'delete user successful'
            else:
                code = 500
                data = {}
                message = 'delete user  failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/add_user', AddUserHnadler),
    ('/api/update_user', UpdateUserHandler),
    ('/api/get_user', GetUserHandler),
    ('/api/delete_user', DeleteUserHandler),
]