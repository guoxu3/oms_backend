#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    log out handler
    clear cookie
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *


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
            try:
                self.set_secure_cookie("access_token", "")
            except:
                ok = False
                info = "log out failed"
            else:
                ok = True
                info = "log out successful"
        else:
            ok = True
            info = "Not log in yet"

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass

handlers = [
    ('/api/logout', LogoutHandler),
]