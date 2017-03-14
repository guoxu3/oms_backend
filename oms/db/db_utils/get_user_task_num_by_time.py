#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db._db_init import Task
from lib.logger import log
from peewee import *


def get_user_task_num_by_time(begin_time=0, end_time=0, username=None):
    if begin_time == 0 or end_time == 0 or begin_time > end_time or not username:
        return False

    user_task_statistic = {}
    query = (Task
             .select(Task.creator, fn.COUNT(Task.task_id).alias('task_sum'),
                     fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
             .where(
                    (Task.creator == username) &
                    (Task.create_time >= begin_time) &
                    (Task.create_time <= end_time))
             .group_by(Task.creator, 'create_date'))
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
