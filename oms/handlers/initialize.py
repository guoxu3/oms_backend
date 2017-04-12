#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    initialize handlers
"""

import tornado.web
import tornado.escape
import tornado.ioloop
from lib import verify, encrypt, mail
from db import db_machine
from lib.salt_api import SaltAPI as sapi
import json
import check
from lib.logger import log
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class InitializeHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(5)

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(InitializeHandler, self).__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.token = self.get_secure_cookie("access_token")
        self.handler_permission = '8'
        self.get_permission = '8.1'
        self.post_permission = '8.2'

    def get(self):
        ip = self.get_argument('ip', None)
        software = self.get_argument('software', None)
        status = self.get_argument('status', 0)
        result = db_machine.update_initialize_status(ip, software, status)
        if result:
            ok = True
            info = 'Update initialize status successful'
        else:
            ok = False
            info = 'Update initialize status failed'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    def post(self):
        post_initialize_permission = '8.2.1'
        post_install_permission = '8.2.2'

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
        if action == 'initialize':
            local_permission_list = [self.handler_permission, self.post_permission, post_initialize_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            tornado.ioloop.IOLoop.instance().add_callback(self.machine_initialize(data['ip']))
            ok = True
            info = "Initializing..."
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        if action == 'install':
            local_permission_list = [self.handler_permission, self.post_permission, post_install_permission]
            ok, info, _ = verify.has_permission(self.token, local_permission_list)
            if not ok:
                self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
                return

            tornado.ioloop.IOLoop.instance().add_callback(self.install_software(data['ip'], data['software']))
            ok = True
            info = 'Software installing...'
            self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))
            return

        ok = False
        info = 'Unsupported task action'
        self.finish(tornado.escape.json_encode({'ok': ok, 'info': info}))

    @run_on_executor
    def machine_initialize(self, ip):
        result = sapi.run_script([ip], 'salt://scripts/initialize.sh', 'initialize')
        log.info(result)

    @run_on_executor
    def install_software(self, ip, software):
        result = sapi.run_script([ip], 'salt://scripts/install_software.sh', software)
        log.info(result)

    def options(self):
        pass


handlers = [
    ('/api/initialize', InitializeHandler),
]
