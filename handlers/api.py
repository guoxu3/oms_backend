#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.db_action import *
import uuid


# 生成task_id,将数据写进数据库
class CreatTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        headers_dict = dict(self.request.headers)
        content_type = headers_dict['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            task_id = uuid.uuid1().hex
            #result = insert_task_data(body)
            result = 'ok'
            data = {
                'task_id': task_id,
                'result':  result
            }

            response = {'code': 200,
                        'data': data,
                        'message': 'ok'
                        }
            print response
        else:
            response = {'code': 400,
                        'data': '',
                        'message': 'body or content-type format error'
                        }
        self.write(tornado.escape.json_encode(response))


# 获取task信息,显示在页面上
class GetTaskInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        data = select_task_id('1111')
        response = {'code': 200,
                    'data': data,
                    'message': 'ok'
                    }
        self.write(tornado.escape.json_encode(response))



# 读取mysql 获取当前的更新状态
class GetStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, id):
        if not is_number(id):
            response = {'code': 400,
                        'data': '{}',
                        'message': 'id must be digits'
                        }
        else:
            data = select_task_id('1111')
            response = {'code': 200,
                        'data': data,
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
            response = {'code': 200,
                        'data': '{}',
                        'message': 'ok'
                        }
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
           response = {'code': 200,
                        'data': '{}',
                        'message': 'ok'
                        }
        else:
            response = {'code': 400,
                        'data': '',
                        'message': 'body or content-type format error'
                        }
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/get_task_info', GetTaskInfoHandler),
    ('/api/create_task', CreatTaskHandler),
    ('/api/get_status/id=(.*$)', GetStatusHandler),
    ('/api/update', UpdateHandler),
    ('/api/update_status', UpdateStatusHandle)
]
