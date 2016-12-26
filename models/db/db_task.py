#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义task表相关的操作
"""

from peewee import *
from _db_init import *
from lib.logger import log
import db_task_status


# 获取总数量
def row_count():
    try:
        count = Task.select().count()
    except Exception, e:
        log.exception('exception')
        return 0
    else:
        return count


# 插入数据到task表
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
        task_status_dict = {'task_id': task_dict['task_id'],
                            'start_time': 0,
                            'revert_time': 0,
                            'status': 0,
                            'percent': 0,
                            'revert': 0
                            }
        if db_task_status.add(task_status_dict):
            return True
        else:
            return False


# 获取task信息
def get(task_id=None, start=0, count=10):
    if task_id:
        try:
            info = Task.select().where(Task.task_id == task_id).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in Task.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


# 更新task
def update(update_dict):
    task = Task.get(task_id=update_dict['task_id'])
    for key in update_dict:
        if key != 'task_id':
            setattr(task, key, update_dict[key])
    try:
        task.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 删除 task
def delete(task_id):
    del_data = (Task
                .delete()
                .where(Task.task_id == task_id))
    try:
        del_data.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        if db_task_status.delete(task_id):
            return True
        else:
            return False
