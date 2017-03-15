#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db._db_init import Task
from lib.logger import log
from peewee import *


def get_task_statistic_by_time(begin_time=0, end_time=0, username=None):
    if begin_time == 0 or end_time == 0 or begin_time > end_time:
        return False

    user_task_statistic = {}
    if username:
        query = (Task
                 .select(fn.COUNT(Task.task_id).alias('task_sum'),
                         fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
                 .where(
                        (Task.creator == username) &
                        (Task.create_time >= begin_time) &
                        (Task.create_time <= end_time))
                 .group_by(SQL('create_date')))
        try:
            for info in query.execute():
                print info
                task_sum = info.__dict__['task_sum']
                create_date = info.__dict__['create_date']
                user_task_statistic[create_date] = task_sum

        except Exception:
            log.exception('exception')
            return False
        else:
            return user_task_statistic
    else:
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
        except Exception:
            log.exception('exception')
            return False
        else:
            return user_task_statistic
