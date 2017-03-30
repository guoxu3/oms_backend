#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 use salt api，you need to install salt on your server first
 salt documentation：
    https://docs.saltstack.com/en/latest/contents.html
 salt api documentation：
    https://docs.saltstack.com/en/latest/topics/api.html

"""

import salt.client
from lib.logger import log


class SaltAPI:
    def __init__(self):
        pass
        # todo

    @staticmethod
    def run_script(tgt, script_path, script_arg):
        """
        tgt : a list, ie. ['host1', 'host2', ....],can not be ['*']
        script_path: string, ie. salt://scripts/test.sh or /srv/run/scripts/test.sh
        script_args: a list, ie. ['arg1', 'arg2' ,'arg3',....]
        """
        client = salt.client.LocalClient()
        try:
            result = client.cmd(tgt, 'cmd.script', [script_path, '"%s"' % script_arg], expr_form='list')
        except Exception:
            log.exception('exception')
        else:
            return result
