#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db import db_utils


def check_admin(token):
    permissions = db_utils.get_info_by_token(token)['permissions']
    permission_list = []
    for permission in permissions.split(','):
        permission_list.append(permission)
    if '0' in permission_list:
        return True
    else:
        return False
