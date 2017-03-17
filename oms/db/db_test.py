#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from playhouse.pool import PooledMySQLDatabase

# mysql connection pool
db = PooledMySQLDatabase(
    database='oms',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    charset='utf8',
    max_connections=20,
    stale_timeout=300
)


# base model
class BaseModel(Model):
    class Meta:
        database = db


# task table
class Task(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    creator = CharField()
    ip = CharField()
    create_time = IntegerField()
    target = CharField()
    version = IntegerField()
    type = CharField()
    content = CharField()
    description = CharField()
    executor = CharField()
    status = BooleanField()
    start_time = IntegerField()
    revert_time = IntegerField()
    percent = IntegerField()
    revert = BooleanField()

    class Meta:
        db_table = 'task'


# user table
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


# permissions table
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = CharField(unique=True)

    class Meta:
        db_table = 'permissions'


def get_user_task_num_by_time(begin_time=0, end_time=0):
    user_list = []
    for a in User.select(User.username):
        user_list.append(a.__dict__['_data']['username'])
    user_task_statistic = {}
    query = (Task
             .select(Task.creator, fn.COUNT(Task.task_id).alias('task_sum'),
                     fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
             .where(
                    (Task.create_time >= begin_time) &
                    (Task.create_time <= end_time))
             .group_by(Task.creator, SQL('create_date')))
    try:
        for info in query.execute():
            creator = info.__dict__['_data']['creator']
            task_sum = info.__dict__['task_sum']
            create_date = info.__dict__['create_date']
            if create_date not in user_task_statistic:
                user_task_statistic[create_date] = {creator: task_sum}
            else:
                user_task_statistic[create_date][creator] = task_sum
        print user_task_statistic, user_list
    except Exception:

        return False
    else:
        return user_task_statistic, user_list


def get_permission(is_all=False, start=0, count=10):
    data_list = []
    if is_all:
        try:
            for info in Permissions.select():
                _data = info.__dict__['_data']
                permission_code = _data['permission_code']
                if len(permission_code) == 1:
                    pid = '0'
                else:
                    pid = '.'.join(permission_code.split('.')[:-1])

                name = _data['permission_desc'] + '[' + _data['permission'] + ']' + '[' + _data['permission_code'] + ']'
                permission_dcit = {
                    'id': permission_code,
                    'pId': pid,
                    'name': name
                }
                data_list.append(permission_dcit)
        except Exception:
            return False
        else:
            return data_list
    else:
        try:
            for info in Permissions.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception:
            return False
        else:
            return data_list

get_permission(True)
