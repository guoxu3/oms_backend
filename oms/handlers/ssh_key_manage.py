#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    ssh-key manage handlers
"""

import tornado.web
import tornado.escape
from lib import verify, encrypt, mail
from db import db_ssh_key_info, db_user
from lib.salt_api import SaltAPI as sapi
import json
import check


class SshKeyManageHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(SshKeyManageHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.token = self.get_secure_cookie("access_token")
        self.handler_permission = '7'
        self.get_permission = '7.1'
        self.post_permission = '7.2'
        self.delete_permission = '7.3'

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

        mode = self.get_argument('mode', None)
        username = self.get_argument('username', None)
        ip = self.get_argument('ip', None)
        key_info = db_ssh_key_info.get(mode, username, ip)
        if key_info is not False:
            ok = True
            info = {'data': key_info}
        else:
            ok = False
            info = 'Get ssh-key info failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_add_permission = '7.2.1'
        post_delete_permission = '7.2.1'

        ok, info = check.check_login(self.token)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok, info = check.check_content_type(self.request)
        if not ok:
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        body = json.loads(self.request.body)
        action, ssh_key_data = body['action'], body['data']
        if action == 'add':
            local_permission_list = [self.handler_permission, self.post_permission, post_add_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            ip = ssh_key_data['ip']
            ssh_key_string = db_user.get(username=ssh_key_data['username'])
            encrypt_ssh_key_info = encrypt.base64_encode(ssh_key_data['system_user'] + '@' +
                                                         ssh_key_string + " " + ssh_key_data['username'])
            result = sapi.run_script([ip], 'salt://scripts/add_ssh_key.sh', encrypt_ssh_key_info)
            retcode = result[ip]['retcode']

            if retcode == 0:
                if db_ssh_key_info.add(ssh_key_data):
                    ok = True
                    info = 'Add ssh-key successful'
                else:
                    ok = False
                    info = 'Add ssh-key failed'
            else:
                ok = False
                info = 'Add ssh-key failed'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if action == 'delete':
            local_permission_list = [self.handler_permission, self.post_permission, post_delete_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            fail_count = 0
            for ssh_key_info in ssh_key_data:
                ip = ssh_key_info['ip']
                encrypt_ssh_key_info = encrypt.base64_encode(ssh_key_info['system_user'] + '@' +
                                                             ssh_key_info['username'])
                result = sapi.run_script([ip], 'salt://scripts/delete_ssh_key.sh', encrypt_ssh_key_info)
                retcode = result[ip]['retcode']
                if retcode == 0:
                    if db_ssh_key_info.delete(ssh_key_info['username'], ssh_key_info['ip'], ssh_key_info['system_user']):
                        fail_count += 0
                    else:
                        fail_count += 1
                else:
                    fail_count += 1

            if fail_count == 0:
                ok = False
                info = 'Delete all ssh-key info failed'
            else:
                ok = False
                info = 'Delete some ssh-key info failed, please retry'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported ssh-key action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def options(self):
        pass


handlers = [
    ('/api/ssh_key_manage', SshKeyManageHandler),
]
