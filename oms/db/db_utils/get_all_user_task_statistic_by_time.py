#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db._db_init import Task, User
from lib.logger import log
from peewee import *


def get_all_user_task_statistic_by_time(begin_time=0, end_time=0):
    if begin_time == 0 or end_time == 0 or begin_time > end_time:
        return False

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
    except Exception:
        log.exception('exception')
        return False
    else:
        return user_task_statistic, user_list
