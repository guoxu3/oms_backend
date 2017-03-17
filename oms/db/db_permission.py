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


def get(is_all=False, start=0, count=10, permission=None):
    data_list = []
    if is_all:
        try:
            for info in Permissions.select():
                _data = info.__dict__['_data']
                permission_code = _data['permission_code']
                if len(permission_code) == 1:
                    pid = '0'
                    opened = True
                else:
                    pid = '.'.join(permission_code.split('.')[:-1])
                    opened = False
                name = _data['permission_desc'] + '--[' + _data['permission'] + ']' + '--[' + _data['permission_code'] + ']'
                permission_dcit = {
                    'id': permission_code,
                    'pId': pid,
                    'name': name,
                    'open': opened
                }
                data_list.append(permission_dcit)
        except Exception:
            return False
        else:
            return data_list
    else:
        if permission:
            try:
                info = Permissions.select().where(Permissions.permission == permission).get()
            except Exception:
                log.exception('exception')
                return False
            else:
                return info.__dict__['_data']
        else:
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


def update(permissions_dict):
    permission = Permissions.get(permisson=permissions_dict['permission'])
    for key in update_dict:
        if key != 'permission':
            setattr(permission, key, permissions_dict[key])
    try:
        permission.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def delete(permisson):
    del_data = (Permissions
                .delete()
                .where(Permissions.permission == permisson))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True
