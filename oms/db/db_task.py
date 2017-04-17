#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    task table operation
"""


from _db_init import *
from lib.logger import log


def row_count():
    try:
        count = Task.select().count()
    except Exception:
        log.exception('exception')
        return 0
    else:
        return count


def add(task_dict):
    task = Task()
    for key in task_dict:
        setattr(task, key, task_dict[key])
    try:
        task.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def get(task_id=None, start=0, count=10):
    if task_id:
        try:
            info = Task.select().order_by(Task.id).where(Task.task_id == task_id).get()
        except Exception:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in Task.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception:
            log.exception('exception')
            return False
        else:
            return data_list


def update(update_dict):
    task = Task.get(task_id=update_dict['task_id'])
    for key in update_dict:
        if key != 'task_id':
            setattr(task, key, update_dict[key])
    try:
        task.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def delete(task_id):
    del_data = (Task
                .delete()
                .where(Task.task_id == task_id))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True
