#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义permission表的相关操作
"""

from peewee import *
from _db_init import *
from lib.logger import log


# 获取总数量
def row_count():
    try:
        count = Permissions.select().count()
    except Exception, e:
        log.exception('exception')
        return 0
    else:
        return count


# 获取权限信息
def get(start=0, count=10):
    data_list = []
    try:
        for info in Permissions.select().offset(start).limit(count):
            data_list.append(info.__dict__['_data'])
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return data_list


# 插入数据到permissions表中
def add(permissions_dict):
    permissions = Permissions()
    for key in permissions_dict:
        setattr(permissions, key, permissions_dict[key])
    try:
        permissions.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True
