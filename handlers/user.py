#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from lib.judgement import *
from lib import db
import uuid
import json
import time


# user handler
class UserHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        mail = self.get_argument('mail')
        user_info = db.get_user(mail)
        if user_info:
            code = 200
            data = user_info
            message = 'get user successful'
        else:
            code = 500
            data = {}
            message = 'no such a user'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            data = {}
            message = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                user_data = data
                if db.insert_user(user_data):
                    code = 200
                    data = {}
                    message = 'add user successful'
                else:
                    code = 500
                    data = {}
                    message = 'add user failed'
            elif action == 'update':
                user_data = data
                if db.update_user(user_data):
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
                message = 'unsupported user action'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        user_id = self.get_argument('user_id')

        if db.delete_user:
            code = 200
            data = {}
            message = 'delete user successful'
        else:
            code = 500
            data = {}
            message = 'delete user failed'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/user', UserHandler),
]