#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
api handlers
"""

import tornado.web
import tornado.escape
from lib import verify, encrypt, mail
from lib.salt_api import SaltAPI as sapi
from db import db_task, db_machine
import utils
import json
import check


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

    def get(self):
        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        local_permission_list = [self.handler_permission, self.get_permission]
        ok, info, _ = verify.has_permission(self.token, local_permission_list)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        task_id = self.get_argument('task_id', None)
        if not task_id:
            ok = False
            info = 'Must have task_id'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        task = db_task.get(task_id)
        result = sapi.run_script([task['ip']], 'salt://scripts/get_task_log.sh', [task_id])
        retcode = result[task['ip']]['retcode']
        if retcode == 0:
            log_info = result[task['ip']]['stdout']
            ok = True
            info = {'data': log_info}
        else:
            ok = False
            info = 'Get Log info Failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_update_file_permission = '5.2.1'
        post_update_db_permission = '5.2.2'

        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = check.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, data = body['action'], body['data']
        task = db_task.get(data['task_id'])
        update_type = task['type']
        excutor = self.get_cookie("username")

        if action == 'update':
            local_permission_list = [self.handler_permission, self.post_permission]
            if update_type == 'update_file':
                local_permission_list = [self.handler_permission, self.post_permission, post_update_file_permission]
            if update_type == 'update_db':
                local_permission_list = [self.handler_permission, self.post_permission, post_update_db_permission]

            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            encode_update_string = encrypt.base64_encode(task['task_id'] + '@' + task['type'] +
                                                         "@" + task['target'] + "@" + str(task['version']) +
                                                         "@" + task['content'])

            if task['status'] is True:
                ok = False
                info = 'Task has been executed'
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

            task_status = {'task_id': task['task_id'], 'status': 1,
                           'start_time': utils.cur_timestamp(), 'executor': excutor}
            if not db_task.update(task_status):
                ok = False
                info = 'update task status failed'
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

            result = sapi.run_script([task['ip']], 'salt://scripts/update.sh', [encode_update_string])
            retcode = result[task['ip']]['retcode']
            if retcode == 0:
                ok = True
                info = 'Execute update script successful'
            else:
                ok = False
                info = 'Execute update script failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

        if action == 'revert':
            local_permission_list = [self.handler_permission, self.post_permission]
            if update_type == 'update_file':
                local_permission_list = [self.handler_permission, self.post_permission, post_update_file_permission]
            if update_type == 'update_db':
                local_permission_list = [self.handler_permission, self.post_permission, post_update_db_permission]

            ok, info, is_admin = verify.has_permission(self.token, local_permission_list)
            if not is_admin:
                info = "Only admin can revert."
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            encode_update_string = encrypt.base64_encode(task['task_id'])
            task_status = {'task_id': task['task_id'], 'revert': 1,
                           'revert_time': utils.cur_timestamp()}
            if not db_task.update(task_status):
                ok = False
                info = 'update task status failed'
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

            result = sapi.run_script([task['ip']], 'salt://scripts/revert.sh', [encode_update_string])
            retcode = result[task['ip']]['retcode']
            if retcode == 0:
                ok = True
                info = 'Execute revert script successful'
            else:
                ok = False
                info = 'Execute revert script failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

        ok = False
        info = 'Unsupported update action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/update', UpdateHandler),
]
