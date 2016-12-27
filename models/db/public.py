#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
一些通用的db类的操作
"""

from _db_init import *
import db_session,db_user
from lib.common import *
from lib.logger import log


# 通过传入的session值获取用户名、过期时间、以及权限
def get_info_by_session(access_token):
    data = db_session.get(access_token)
    data['permissions'] = db_user.get(data['username'])['permissions']
    return data


# 判断是否具有权限
def has_permission(access_token, handler_permission):
    permission_list = list(get_info_by_session(access_token)['permissions'])
    expire_time = get_info_by_session(access_token)['expire_time']
    if cur_timestamp() > expire_time:
        return {'ok': False, 'info': 'please login agin'}
    if handler_permission not in permission_list:
        return {'ok': False, 'info': 'no permission'}
