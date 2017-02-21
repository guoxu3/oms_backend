#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib import verify, common, encrypt, mail
from models.salt_api import SaltAPI as sapi
from models.db import db_task, db_machine
import json
import public


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
        self.token = self.get_secure_cookie("access_token")


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

        ok, info = public.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = public.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.load(self.request.body)
        action, data = body['action'], body['data']
        if action == 'update_file':
            task_id = data['task_id']
            username = ''
            task = db_task.get(task_id)
            encode_update_string = encrypt.base64_encode(username + '@' + task['repository'] + "@" + task['content'])
            task_status = {'task_id': task_id, 'status': 1, 'start_time': common.cur_timestamp(), 'executor': username}
            db_task.update(task_status)
            result = sapi.run_script(task['ip'], 'salt://scripts/update_file.sh', encode_update_string)
            if result:
                ok = True
                info = 'Execute script successful'
            else:
                ok = False
                info = 'Execute script failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        elif action == 'update_db':
            # todo
            ok = ''
            info = ''
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported update action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/update', UpdateHandler),
]
