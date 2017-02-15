#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    user login handler
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from models.db import db_user,db_permission,db_session
from lib import encrypt
from lib import config
import json


class LoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    def get(self):
        token = self.get_secure_cookie("access_token")
        if token:
            if is_expired(token):
                ok = False
                info = "login time out"
            else:
                ok = True
                info = ""
        else:
            ok = False
            info = "please login first"

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

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
            # get saved passwd and salt value from database, and compare with user input
            saved_user_data = db_user.get(username)
            if saved_user_data:
                saved_salt = saved_user_data['salt']
                saved_passwd = saved_user_data['passwd']
                _, encrypt_passwd = encrypt.md5_salt(password, saved_salt)
                if saved_passwd == encrypt_passwd:
                    # create access_token and save in database
                    access_token = encrypt.make_cookie_secret()
                    session_data = {'access_token': access_token, 'username': username, 'action_time': cur_timestamp()}
                    session_data['expire_time'] = session_data['action_time'] + config.expire_second
                    if db_session.update(session_data):
                        self.set_secure_cookie("access_token", access_token)
                        self.set_cookie("username", username)
                        ok = True
                        info = {}
                    else:
                        ok = False
                        info = "error ,please contact with the system administrator"
                else:
                    ok = False
                    info = 'password error'
            else:
                ok = False
                info = 'no such a user'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/login', LoginHandler),
]