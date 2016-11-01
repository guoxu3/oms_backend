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
import time


# 生成task_id,将数据写进数据库
class AddTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            task_info = json.loads(body)
            # data['task_id'] = uuid.uuid1().hex
            task_info['task_id'] = '0358c3c78f5211e685855cf9389306a2'

            if db.insert_task(task_info):
                code = 200
                data = {'task_id': task_info['task_id']}
                message = 'add task successful'
            else:
                code = 500
                data = {}
                message = 'add task failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 获取task信息
class GetTaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        task_id = self.get_argument('task_id')
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


# 获取task status
class GetTaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        task_id = self.get_argument('task_id')
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


# 更新task status
class UpdateTaskStatusHandle(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            status = json.loads(body)
            if db.update_task_status(status):
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


# 调用更新脚本
class UpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            # todo
            code = 200
            data = {}
            message = ''
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 添加machine_info
class AddMachineInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            machine_info = json.loads(body)
            if db.insert_machine_info(machine_info):
                code = 200
                data = {}
                message = 'add machine info successful'
            else:
                code = 500
                data = {}
                message = 'add miachine info failed'
        else:
            code = 400
            data = {}
            message = 'body or content-type format error'

        response = dict(code=code, data=data, message=message)
        self.write(tornado.escape.json_encode(response))


# 更新machine info信息
class UpdateMachineInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            machine_info = json.loads(body)
            if db.update_machine_info(machine_info):
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


# 删除machine info
class DeleteMachineInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            machine_name = json.loads(body)['machine_name']
            if db.delete_task(machine_name):
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
    ('/api/get_task', GetTaskHandler),
    ('/api/add_task', AddTaskHandler),
    ('/api/delete_task', DeleteTaskHandler),
    ('/api/get_task_status', GetTaskStatusHandler),
    ('/api/update_task_status', UpdateTaskStatusHandle),
    ('/api/update', UpdateHandler),
    ('/api/add_machine_info', AddMachineInfoHandler),
    ('/api/update_machine_info', UpdateMachineInfoHandler),
    ('/api/delete_machine_info', DeleteMachineInfoHandler),
]
