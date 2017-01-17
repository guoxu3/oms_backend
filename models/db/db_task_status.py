#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    task_status table operation
"""

from peewee import *
from _db_init import *
from lib.logger import log


def row_count():
    try:
        count = TaskStatus.select().count()
    except Exception, e:
        log.exception('exception')
        return 0
    else:
        return count


def add(task_status_dict):
    task_status = TaskStatus()
    for key in task_status_dict:
        setattr(task_status, key, task_status_dict[key])
    try:
        task_status.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def get(task_id=None, start=0, count=10):
    if task_id:
        try:
            info = TaskStatus.select().where(TaskStatus.task_id == task_id).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in TaskStatus.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


def update(update_dict):
    task_status = TaskStatus.get(task_id=update_dict['task_id'])
    for key in update_dict:
        if key != 'task_id':
            setattr(task_status, key, update_dict[key])
    try:
        task_status.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


def delete(task_id):
    del_data = (TaskStatus
                .delete()
                .where(TaskStatus.task_id == task_id))
    try:
        del_data.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True
