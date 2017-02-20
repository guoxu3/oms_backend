#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    log out handler
    clear cookie
"""

import tornado.web
import tornado.escape


class LogoutHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(LogoutHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    def get(self):
        if self.get_secure_cookie("access_token"):
            self.set_secure_cookie("access_token", "")
            ok = True
            info = "Logout successful"
        else:
            ok = True
            info = "Not login yet"
        self.write(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass

handlers = [
    ('/api/logout', LogoutHandler),
]
