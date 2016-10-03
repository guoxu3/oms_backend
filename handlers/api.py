#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""


import tornado.web
import tornado.escape
from lib import judgement


class GetHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        aa = dict(a=1, b=2, c=3)
        bb = tornado.escape.json_encode(aa)
        self.write(bb)


class PostHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        headers_dict = dict(self.request.headers)
        content_type = headers_dict['Content-Type']
        if content_type == 'application/json':
            print "right"

        body = self.request.body
        if judgement.is_json(body):
            print "aaaa"

handlers = [
    ('/api/get', GetHandler),
    ('/api/post', PostHandler)
]