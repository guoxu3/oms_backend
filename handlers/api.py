#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from models.db import db_task,db_task_status,db_machine
import uuid
import json
import time, datetime


# task handler 处理task相关操作
from python.sd3a.lib.common import cur_timestamp


class TaskHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    # get 获取task信息
    def get(self):
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if task_id:
            task_info = db_task.get(task_id)
        else:
            task_info = db_task.get(task_id, start, count)

        if task_info:
            ok = True
            info = {'data': task_info, 'count': db_task.row_count()}
        else:
            ok = False
            info = 'no such a task'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    # post 新增或者更新操作，接收json,操作类型由action定义
    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            ok = False
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                task_data = data
                task_data['task_id'] = uuid.uuid1().hex
                task_data['create_time'] = cur_timestamp()
                # task_data['task_id'] = '0358c3c78f5211e685855cf9389306a2'
                if db_task.add(task_data):
                    ok = True
                    info = {'task_id': task_data['task_id']}
                else:
                    ok = False
                    info = 'add task failed'
            else:
                ok = False
                info = 'unsupported task action'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    # delete 删除task信息
    def delete(self):
        task_id = self.get_argument('task_id')
        if db.get_task(task_id):
            if db_task.delete(task_id):
                ok = True
                info = 'delete task successful'
            else:
                ok = False
                info = 'delete task failed'
        else:
            ok = False
            info = 'no such a task'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


# task status handler  处理task_status相关操作
class TaskStatusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(TaskStatusHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    # get 获取task_status信息
    def get(self):
        task_id = self.get_argument('task_id', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if task_id:
            task_status_info = db_task_status.get(task_id)
        else:
            task_status_info = db_task_status.get(task_id, start, count)

        if task_status_info:
            ok = True
            info = {'data': task_status_info, 'count': db_task_status.row_count()}
        else:
            ok = False
            info = 'no such a task status'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    # post 新增或更新等操作，接收json,操作类型由action定义
    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            ok = False
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'update':
                task_status_data = data
                if db_task_status.update(task_status_data):
                    ok = True
                    info = 'update task status successful'
                else:
                    ok = False
                    info = 'update task status failed'
            else:
                ok = False
                info = 'unsupported task status action'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


# machine info handler
class MachineInfoHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(MachineInfoHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    def get(self):
        machine_name = self.get_argument('machine_name', None)
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        if machine_name:
            machine_info = db_machine.get(machine_name)
        else:
            machine_info = db_machine.get(machine_name, start, count)

        if machine_info:
            ok = True
            info = {'data': machine_info, 'count': db_machine.row_count*()}
        else:
            ok = False
            info = 'no such a machine info'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if not is_content_type_right(content_type) or not is_json(body):
            ok = False
            info = 'body or content-type format error'
        else:
            body = json.loads(body)
            action, data = body['action'], body['data']
            if action == 'add':
                machine_info_data = data
                if db_machine.add(machine_info_data):
                    ok = True
                    info = 'add machine info successful'
                else:
                    ok = False
                    info = 'add miachine info failed'
            elif action == 'update':
                machine_info_data = data
                if db_machine.add(machine_info_data):
                    ok = True
                    info = 'update task status successful'
                else:
                    ok = False
                    info = 'update task status failed'
            else:
                ok = False
                info = 'unsupported task status action'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def delete(self):
        machine_name = self.get_argument('machine_name')
        if db_machine.delete(machine_name):
            ok = True
            info = 'delete task successful'
        else:
            ok = False
            info = 'delete task  failed'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


# 调用更新脚本
class UpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UpdateHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        content_type = dict(self.request.headers)['Content-Type']
        body = self.request.body
        if is_content_type_right(content_type) and is_json(body):
            # todo
            ok = True
            info = ''
        else:
            ok = False
            info = 'body or content-type format error'

        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


handlers = [
    ('/api/task', TaskHandler),
    ('/api/task_status', TaskStatusHandler),
    ('/api/update', UpdateHandler),
    ('/api/machine_info', MachineInfoHandler),
]
