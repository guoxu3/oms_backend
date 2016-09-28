#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape
import textwrap


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
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


handlers = [
    ('/api/get', GetHandler),
    ('/api/post', PostHandler)
]