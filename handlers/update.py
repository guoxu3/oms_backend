#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib.judgement import *
from lib.common import *
from lib.encrypt import *
from models.salt_api import SaltAPI as sapi
from models.db import db_task,db_task_status,db_machine
import uuid
import json


# 调用更新脚本
class UpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(UpdateHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.handler_permission = '5'
        self.get_permission = '5.1'
        self.post_permission = '5.2'
        self.ok = True
        self.info = ""
        self.token = self.get_secure_cookie("access_token")
        if self.token:
            if is_expired(self.token):
                self.ok = False
                self.info = "login time out"
        else:
            self.ok = False
            self.info = "please login first"

    def post(self):
        post_pay_permission = '5.2.1'
        post_static_permission = '5.2.2'
        post_exp_permission = '5.2.3'
        post_exp_v4_permission = '5.2.4'
        post_sample_api_permission = '5.2.5'
        post_sample_api_v4_permission = '5.2.6'
        post_card_permission = '5.2.7'
        post_channel_permission = '5.2.8'
        post_ground_permission = '5.2.9'
        post_api_permission = '5.2.10'
        post_stock_permission = '5.2.11'
        if self.ok:
            if has_permission(self.token, local_permission):
                content_type = dict(self.request.headers)['Content-Type']
                body = self.request.body
                if is_content_type_right(content_type) and is_json(body):
                    body = json.load(body)
                    action, data = body['action'], body['data']
                    if action == 'update':
                        task_id = data['task_id']
                        username = ''
                        task = db_task.get(task_id)
                        encode_update_string = base64_encode(username + '@' + task['repository'] + "@" + task['content'])
                        task_status = {'task_id': task_id, 'status': 1, 'start_time': cur_timestamp(), 'executor': username}
                        db_task_status.update(task_status)
                        result = sapi.run_script(task['ip'], 'salt://scripts/update_file.sh', encode_update_string)
                        if result:
                            ok = True
                            info = 'run script successful'
                        else:
                            ok = False
                            info = 'run script failed'
                    elif action == 'revert':
                        pass
                        # todo
                    else:
                        ok = False
                        info = 'unsupported task action'
                    # todo
                    ok = True
                    info = ''
                else:
                    ok = False
                    info = 'body or content-type format error'
            else:
                ok = False
                info = 'no permission'
        else:
            ok = self.ok
            info = self.info


        response = dict(ok=ok, info=info)
        self.write(tornado.escape.json_encode(response))

    def options(self):
        pass


handlers = [
    ('/api/update', UpdateHandler),
]
