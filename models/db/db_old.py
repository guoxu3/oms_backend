#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
db action used peewee ORM
"""

from peewee import *
from playhouse.pool import PooledMySQLDatabase
import config
from logger import log

# mysql 连接池
db = PooledMySQLDatabase(
    database=config.dbname,
    host=config.dbhost,
    port=config.dbport,
    user=config.dbuser,
    passwd=config.dbpass,
    charset='utf8',
    max_connections=20,
    stale_timeout=300
    )


# 定义基础类，指定所在的数据库
class BaseModel(Model):
    class Meta:
        database = db


# 定义task表
class Task(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    ip = CharField()
    create_time = IntegerField()
    action = CharField()
    content = CharField()
    description = CharField()

    class Meta:
        db_table = 'task'


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


# 定义machine_info表
class MachineInfo(BaseModel):
    id = IntegerField()
    machine_name = CharField(unique=True)
    inside_ip = CharField()
    outside_ip = CharField()
    usage = CharField()
    is_initialized = IntegerField()
    location = CharField()

    class Meta:
        db_table = 'machine_info'


# 定义user表
class User(BaseModel):
    id = IntegerField()
    mail = CharField(unique=True)
    username = CharField(unique=True)
    passwd = CharField()
    salt = CharField()
    department = CharField()
    permissions = CharField()

    class Meta:
        db_table = 'user'


# 定义权限表Permissions
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = IntegerField()

    class Meta:
        db_table = 'permissions'


# 插入数据到task表
def insert_task(task_dict):
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
        if insert_task_status(task_status_dict):
            return True
        else:
            return False


# 插入数据到task_status表
def insert_task_status(task_status_dict):
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


# 获取task信息
def get_task(task_id=None, start=0, count=10):
    if task_id:
        try:
            info = Task.select().where(Task.task_id == task_id).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
        finally:
            db.close()
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


# 获取task_status信息
def get_task_status(task_id=None, start=0, count=10):
    if task_id:
        try:
            info = TaskStatus.select().where(TaskStatus.task_id == task_id).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
        finally:
            db.close()
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
def update_task_status(update_dict):
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


# 删除 task
def delete_task(task_id):
    delete = (Task
              .delete()
              .where(Task.task_id == task_id))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        if delete_task_status(task_id):
            return True
        else:
            return False


# 删除 task_status
def delete_task_status(task_id):
    delete = (TaskStatus
              .delete()
              .where(TaskStatus.task_id == task_id))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 插入数据到machine_info表
def insert_machine_info(machine_info_dict):
    machine_info = MachineInfo()
    for key in machine_info_dict:
        setattr(machine_info, key, machine_info_dict[key])
    try:
        machine_info.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 获取machine_info信息
def get_machine_info(machine_name=None, start=0, count=10):
    if machine_name:
        try:
            info = MachineInfo.select().where(MachineInfo.machine_name == machine_name).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
        finally:
            db.close()
    else:
        data_list = []
        try:
            for info in MachineInfo.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


# 更新machine_info数据
def update_machine_info(machine_info_dict):
    machine_info = TaskStatus.get(machine_name=machine_info_dict['machine_name'])
    for key in machine_info_dict:
        if key != 'machine_name':
            setattr(machine_info, key, machine_info_dict[key])
    try:
        machine_info.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 删除machine_info数据
def delete_machine_info(machine_name):
    delete = (MachineInfo
              .delete()
              .where(MachineInfo.machine_name == machine_name))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False


# 获取用户信息
def get_user(username=None, start=0, count=10):
    if username:
        try:
            info = User.select().where(User.username == username).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
        finally:
            db.close()
    else:
        data_list = []
        try:
            for info in User.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


# 插入数据到user表中
def insert_user(user_dict):
    user = User()
    for key in user_dict:
        setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 更新用户信息
def update_user(user_dict):
    user = User.get(username=user_dict['username'])
    for key in user_dict:
        if key != 'username':
            setattr(user, key, user_dict[key])
    try:
        user.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 删除用户
def delete_user(username):
    delete = (User
              .delete()
              .where(User.username == username))
    try:
        delete.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        if get_user(username):
            return False
        else:
            return True
