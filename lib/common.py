#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
通用函数
"""

import time
import datetime
from lib import config
from models.db import db_session


# 将unicode 转换为str
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# 获取当前的时间戳
def cur_timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


# 每次操作时更新时间
def update_timestamp(access_token):
    session_data = {'access_token': access_token, 'action_time': cur_timestamp()}
    session_data['expire_time'] = session_data['action_time'] + config.expire_second
    db_session.update(session_data)