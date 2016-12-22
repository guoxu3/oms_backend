#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
通用函数
"""

import time
import datetime


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
