#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib import db
import uuid
import json


# 生成task_id,将数据写进数据库
class CreatTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            task_info = json.loads(body)
            # data['task_id'] = uuid.uuid1().hex
            task_info['task_id'] = '0358c3c78f5211e685855cf9389306a2'

            if db.create_task(task_info):
                code = 200
                data = {'task_id': task_info['task_id']}
                message = 'create task successful'
            else:
                code = 500
                data = {}
                message = 'create task failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 获取task信息,显示在页面上
class GetTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, task_id):
        task_info = db.get_task(task_id)
        if task_info:
            code = 200
            data = task_info
            message = 'get task successful'
        else:
            code = 500
            data = {}
            message = 'no such a task'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))



# 读取mysql 获取当前的更新状态
class GetTaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, task_id):
        task_status_info = db.get_task_status(task_id)
        if task_status_info:
            code = 200
            data = task_status_info
            message = 'get task status successful'
        else:
            code = 500
            data = {}
            message = 'no such a task status'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 调用更新脚本
class UpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            code = 200
            data = {}
            message = ''
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 供脚本中调用的接口,用来更新当前的更新进度
class UpdateStatusHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            stauts = json.loads(body)
            if db.update_task_status():
                code = 200
                data = {}
                message = 'update task status successful'
            else:
                code = 500
                data = {}
                message = 'update task status failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 删除task
class DeleteTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            task_id = json.loads(body)['task_id']
            if db.delete_task(task_id):
                code = 200
                data = {}
                message = 'delete task successful'
            else:
                code = 500
                data = {}
                message = 'delete task  failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/get_task/id=(.*$)', GetTaskHandler),
    ('/api/create_task', CreatTaskHandler),
    ('/api/get_task_status/id=(.*$)', GetTaskStatusHandler),
    ('/api/update', UpdateHandler),
    ('/api/update_status', UpdateStatusHandle),
    ('/api/delete_task', DeleteTaskHandler),
]
