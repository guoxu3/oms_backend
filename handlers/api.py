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
import time, datetime


# task handler 处理task相关操作
class TaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    # get 获取task信息
    def get(self):
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if task_id:
            task_info = db.get_task(task_id)
        else:
            task_info = db.get_task(task_id, start, count)

        if task_info:
            code = 200
            info = task_info
        else:
            code = 500
            info = 'no such a task'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    # post 新增或者更新操作，接收json,操作类型由action定义
    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                task_data = data
                task_data['task_id'] = uuid.uuid1().hex
                task_data['create_time'] = time.mktime(datetime.datetime.now().timetuple())
                # task_data['task_id'] = '0358c3c78f5211e685855cf9389306a2'
                if db.insert_task(task_data):
                    code = 200
                    info = {'task_id': task_data['task_id']}
                else:
                    code = 500
                    info = 'add task failed'
            else:
                code = 400
                info = 'unsupported task action'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    # delete 删除task信息
    def delete(self):
        task_id = self.get_argument('task_id')
        if db.delete_task(task_id):
            code = 200
            info = 'delete task successful'
        else:
            code = 500
            info = 'delete task failed'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))


# task status handler  处理task_status相关操作
class TaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    # get 获取task_status信息
    def get(self):
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if task_id:
            task_status_info = db.get_task_status(task_id)
        else:
            task_status_info = db.get_task_status(task_id, start, count)

        if task_status_info:
            code = 200
            info = task_status_info
        else:
            code = 500
            info = 'no such a task status'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    # post 新增或更新等操作，接收json,操作类型由action定义
    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'update':
                task_status_data = data
                if db.update_task_status(task_status_data):
                    code = 200
                    info = 'update task status successful'
                else:
                    code = 500
                    info = 'update task status failed'
            else:
                code = 400
                info = 'unsupported task status action'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))


# machine info handler
class MachineInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        machine_name = self.get_argument('machine_name', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if machine_name:
            machine_info = db.get_machine_info(machine_name)
        else:
            machine_info = db.get_machine_info(machine_name, start, count)

        if machine_info:
            code = 200
            info = machine_info
        else:
            code = 500
            info = 'no such a machine info'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            code = 400
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                machine_info_data = data
                if db.insert_machine_info(machine_info_data):
                    code = 200
                    info = 'add machine info successful'
                else:
                    code = 500
                    info = 'add miachine info failed'
            elif action == 'update':
                machine_info_data = data
                if db.update_machine_info(machine_info_data):
                    code = 200
                    info = 'update task status successful'
                else:
                    code = 500
                    info = 'update task status failed'
            else:
                code = 400
                info = 'unsupported task status action'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        machine_name = self.get_argument('machine_name')
        if db.delete_task(machine_name):
            code = 200
            info = 'delete task successful'
        else:
            code = 500
            info = 'delete task  failed'

        response = dict(code=code, info=info)
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
            info = ''
        else:
            code = 400
            info = 'body or content-type format error'

        response = dict(code=code, info=info)
        self.write(tornado.escape.json_encode(response))


handlers = [
    ('/api/task', TaskHandler),
    ('/api/task_status', TaskStatusHandler),
    ('/api/update', UpdateHandler),
    ('/api/machine_info', MachineInfoHandler),
]
