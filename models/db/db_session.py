#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    操作session表
"""


from peewee import *
from _db_conn import BaseModel
from lib.logger import log


# 定义user表
class Session(BaseModel):
    id = IntegerField()
    usename = CharField(unique=True)
    access_token = CharField(unique=True)
    create_time = IntegerField()
    expiration_time = IntegerField()

    class Meta:
        db_table = 'session'


# 获取用户sessions信息
def get(access_token):
    try:
        info = Session.select().where(Session.access_token == access_token).get()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return info.__dict__['_data']


# 插入数据到session表中
def add(session_dict):
    session = Session()
    for key in session_dict:
        setattr(session, key, session_dict[key])
    try:
        session.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 更新session信息
def update(session_dict):
    session = Session.get(username=session_dict['usename'])
    # 如果存在就更新，不存在就新增
    if session:
        for key in session_dict:
            if key != 'username':
                setattr(session, key, session_dict[key])
        try:
            session.save()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return True
    else:
        add(session_dict)


# 删除session信息
def delete(access_token):
    del_data = (Session
                .delete()
                .where(Session.access_token == access_token))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        if get(access_token):
            return False
        else:
            return True
