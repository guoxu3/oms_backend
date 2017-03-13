#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db._db_init import Task
from lib.logger import log


def get_user_task_num_by_time(begin_time=0, end_time=0, username=None):
    if begin_time == 0 or end_time == 0 or begin_time > end_time or not username:
        return False

    data_list = []
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
            data = info.__dict__['_data']
            data['task_sum'] = info.__dict__['task_sum']
            data['create_date'] = info.__dict__['create_date']
    except Exception:
        log.exception('exception')
        return False
    else:
        return data_list
