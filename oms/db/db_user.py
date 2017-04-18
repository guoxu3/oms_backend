#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    user table operation
"""

from peewee import *
from _db_init import *
from lib.logger import log


def row_count():
    try:
        count = User.select().count()
    except Exception:
        log.exception('exception')
        return 0
    else:
        return count


def get(username=None, start=0, count=10):
    if username:
        try:
            info = User.select().where(User.username == username).get()
        except Exception:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in User.select().order_by(User.id).offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception:
            log.exception('exception')
            return False
        else:
            return data_list


def add(user_dict):
    user = User()
    for key in user_dict:
        setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def update(user_dict):
    user = User.get(username=user_dict['username'])
    for key in user_dict:
        if key != 'username':
            setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def delete(username):
    del_data = (User
                .delete()
                .where(User.username == username))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        if get(username):
            return False
        else:
            return True


def get_user_list():
    data_list = []
    try:
        for info in User.select().order_by(User.id):
            data_list.append(info.__dict__['_data']['username'])
    except Exception:
        log.exception('exception')
        return False
    else:
        return data_list
