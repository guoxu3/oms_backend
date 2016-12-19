#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义task_status表相关的操作
"""

from peewee import *
from _db_conn import BaseModel
from ...lib.logger import log


# 定义task_status表
class TaskStatus(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    status = IntegerField()
    start_time = IntegerField()
    revert_time = IntegerField()
    percent = IntegerField()
    revert = IntegerField()

    class Meta:
        db_table = 'task_status'


# 插入数据到task_status表
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


# 获取task_status信息
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


# 更新task_status
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


# 删除 task_status
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
