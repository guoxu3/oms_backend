#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义user表相关的操作
"""

from peewee import *
from _db_conn import BaseModel
from lib.logger import log


# 定义user表
class User(BaseModel):
    id = IntegerField()
    mail = CharField(unique=True)
    username = CharField(unique=True)
    nickname = CharField(unique=True)
    passwd = CharField()
    salt = CharField()
    department = CharField()
    permissions = CharField()

    class Meta:
        db_table = 'user'


# 获取总数量
def row_count():
    try:
        count = User.select().count()
    except Exception, e:
        log.exception('exception')
        return 0
    else:
        return count


# 获取用户信息
def get(username=None, start=0, count=10):
    if username:
        try:
            info = User.select().where(User.username == username).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in User.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


# 插入数据到user表中
def add(user_dict):
    user = User()
    for key in user_dict:
        setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 更新用户信息
def update(user_dict):
    user = User.get(username=user_dict['username'])
    for key in user_dict:
        if key != 'username':
            setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 删除用户
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
