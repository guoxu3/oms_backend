#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    permission table operation
"""

from peewee import *
from _db_init import *
from lib.logger import log


def row_count():
    try:
        count = Permissions.select().count()
    except Exception:
        log.exception('exception')
        return 0
    else:
        return count


def get(start=0, count=10):
    data_list = []
    try:
        for info in Permissions.select().offset(start).limit(count):
            data_list.append(info.__dict__['_data'])
    except Exception:
        log.exception('exception')
        return False
    else:
        return data_list


def add(permissions_dict):
    permissions = Permissions()
    for key in permissions_dict:
        setattr(permissions, key, permissions_dict[key])
    try:
        permissions.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True
