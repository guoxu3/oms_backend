#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
db action used peewee ORM
"""

from peewee import *
import config
from logger import log

db = MySQLDatabase(
    database=config.dbname,
    host=config.dbhost,
    port=config.dbport,
    user=config.dbuser,
    passwd=config.dbpass,
    charset='utf8'
    )


# 定义基础类，指定所在的数据库
class BaseModel(Model):
    class Meta:
        database = db


# 定义task表
class task(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    ip = CharField()
    action = CharField()
    content = CharField()
    description = CharField()


# 定义task_status表
class task_status(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    status = IntegerField()
    percent = IntegerField()
    revert = IntegerField()


# 创建task
def create_task(task_dict):
    db.connect()
    task_data = task(task_id=task_dict['task_id'],
                     ip=task_dict['ip'],
                     action=task_dict['action'],
                     content=task_dict['content'],
                     description=task_dict['description']
                     )
    try:
        task_data.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        task_status_dict = {'task_id': task_dict['task_id'],
                            'status' : 0,
                            'percent': 0,
                            'revert': 0
                            }
        create_task_status(task_status_dict)
    finally:
        db.close()


# 创建task_status
def create_task_status(task_status_dict):
    db.connect()
    task_status_data = task_status(task_id=task_status_dict['task_id'],
                                  status=task_status_dict['status'],
                                  percent=task_status_dict['percent'],
                                  revert=task_status_dict['revert']
                                 )
    try:
        task_status_data.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True
    finally:
        db.close()


# 获取task信息
def get_task(task_id):
    db.connect()
    try:
        info = task.select().where(task.task_id == task_id).get()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return dict(id=info.id,
                    task_id=info.task_id,
                    ip=info.ip,
                    action=info.action,
                    content=info.content,
                    description=info.description
                    )
    finally:
        db.close()


# 获取task_status信息
def get_task_status(task_id):
    db.connect()
    try:
        info = task_status.select().where(task_status.task_id == task_id).get()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return dict(id=info.id,
                    task_id=info.task_id,
                    status=info.status,
                    percent=info.percent,
                    revert=info.revert
                    )
    finally:
        db.close()


# 更新task_status
def update_task_status(update_dict):
    db.connect()
    update = (task_status
              .update(status=update_dict['status'],
                      percent=update_dict['percent'],
                      revert=update_dict['revert'])
                      .where(task_status.task_id == update_dict['task_id']))
    try:
        update.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True
    finally:
        db.close()


# 删除 task
def delete_task(task_id):
    db.connect()
    delete = (task
              .delete()
              .where(task.task_id == task_id))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        delete_task_status(task_id)
    finally:
        db.close()


# 删除 task_status
def delete_task_status(task_id):
    db.connect()
    delete = (task_status
              .delete()
              .where(task_status.task_id == task_id))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True
    finally:
        db.close()
