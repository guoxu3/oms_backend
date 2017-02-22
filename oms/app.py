#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from lib import config
from lib.logger import log


class Application(tornado.web.Application):
    def __init__(self):
        import handlers.urls

        settings = {
            "debug": True,
            "cookie_secret": "sji1fI23fdsffsd1fsdjwrzlHeGfd34nFHdfssfsd"
        }
        super(Application, self).__init__(handlers.urls.handlers, **settings)


def main():
    address = config.address
    port = config.port

    log.info('run server on %s:%s' % (address, port))

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port, address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
