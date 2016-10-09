#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *


# 读取mysql 获取当前的更新状态
class GetStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, id):
        if not is_number(id):
            response = {'code': 400,
                        'data': '',
                        'message': 'id must be digits'
                        }
            self.write(tornado.escape.json_encode(response))
        else:
            response = {'code': 200,
                        'data': '{}',
                        'message': 'ok'
                        }
            self.write(tornado.escape.json_encode(response))


# 更新参数传入,调用更新脚本进行更新
class UpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        headers_dict = dict(self.request.headers)
        content_type = headers_dict['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            # todo
            pass
        else:
            response = {'code': 400,
                        'data': '',
                        'message': 'body or content-type format error'
                        }
            self.write(tornado.escape.json_encode(response))


# 供脚本中调用的接口,用来更新当前的更新进度
class UpdateStatusHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        headers_dict = dict(self.request.headers)
        content_type = headers_dict['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            # todo
            pass
        else:
            response = {'code': 400,
                        'data': '',
                        'message': 'body or content-type format error'
                        }
            self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/get_status/id=(.*$)', GetStatusHandler),
    ('/api/update', UpdateHandler),
    ('/api/update_status', UpdateStatusHandle)
]
