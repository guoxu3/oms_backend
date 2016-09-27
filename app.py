#!/usr/bin/env python
# -*- coding:utf-8 -*-

import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from lib import config


class IndexHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


def main():
    address = config.listen
    port = config.port

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/app", WrapHandler)
        ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port, address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
