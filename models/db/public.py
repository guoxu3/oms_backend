#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
一些通用的db类的操作
"""

from _db_init import *
import db_session,db_user
from lib.common import *
from lib import config
from lib.logger import log


# 通过传入的session值获取用户名、过期时间、以及权限
def get_info_by_session(access_token):
    info = db_session.get(access_token)
    info['permissions'] = db_user.get(info['username'])['permissions']
    return info


# 更新用户最后活动时间和超时间
def update_expire_time(access_token):
    data = {'access_token': access_token, 'action_time': cur_timestamp(), 'expire_time': cur_timestamp() + config.expire_second}
    db_session.update(data)
