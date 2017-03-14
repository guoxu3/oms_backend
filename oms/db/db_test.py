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


def get_user_task_num_by_time(begin_time=0, end_time=0):
    if begin_time == 0 or end_time == 0 or begin_time > end_time :
        return False

    user_task_statistic = {}
    query = (Task
             .select(fn.COUNT(Task.task_id).alias('task_sum'),
                     fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
             .where(
                    (Task.create_time >= begin_time) &
                    (Task.create_time <= end_time))
             .group_by(SQL('create_date')))
    try:
        for info in query.execute():
            task_sum = info.__dict__['task_sum']
            create_date = info.__dict__['create_date']
            user_task_statistic[create_date] = task_sum

        print user_task_statistic

    except Exception as e:
        print e
        print "aaa"
    else:
        return user_task_statistic


get_user_task_num_by_time(1486915200, 1489507199)

