#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    user login handler
"""

import tornado.web
import tornado.escape
from lib import common, encrypt, config, verify
from models.db import db_session
import public
import json


class LoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.token = self.get_secure_cookie("access_token")

    def get(self):
        ok, info = public.check_login(self.token)
        if not ok:
            self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        ok, info = public.check_content_type(self.request)
        if not ok:
            self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        user_info = json.loads(self.request.body)
        username, password = user_info['username'], user_info['passwd']
        ok, info = public.check_password(username, password)
        if not ok:
            self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        access_token = encrypt.make_cookie_secret()
        action_time = common.cur_timestamp()
        session_data = {'access_token': access_token, 'username': username, 'action_time': action_time,
                        'expire_time': action_time + config.expire_second}

        if db_session.update(session_data):
            self.set_secure_cookie("access_token", access_token)
            self.set_cookie("username", username)
            ok = True
            info = {}
        else:
            ok = False
            info = "Login error, please contact with the system administrator"
        self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/login', LoginHandler),
]
