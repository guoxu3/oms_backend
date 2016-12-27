#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from lib import config

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
    creator = CharField()
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
    executor = CharField()
    status = IntegerField()
    start_time = IntegerField()
    revert_time = IntegerField()
    percent = IntegerField()
    revert = IntegerField()

    class Meta:
        db_table = 'task_status'


# 定义machine_info表
class Machine(BaseModel):
    id = IntegerField()
    machine_name = CharField(unique=True)
    inside_ip = CharField()
    outside_ip = CharField()
    usage = CharField()
    is_initialized = IntegerField()
    location = CharField()

    class Meta:
        db_table = 'machine'


# 定义user表
class User(BaseModel):
    id = IntegerField()
    mail = CharField(unique=True)
    username = CharField(unique=True)
    nickname = CharField(unique=True)
    passwd = CharField()
    salt = CharField()
    department = CharField()
    permissions = CharField()

    class Meta:
        db_table = 'user'


# 定义session表
class Session(BaseModel):
    id = IntegerField()
    username = CharField(unique=True)
    access_token = CharField(unique=True)
    create_time = IntegerField()
    expire_time = IntegerField()

    class Meta:
        db_table = 'session'


# 定义权限表Permissions
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = IntegerField(unique=True)

    class Meta:
        db_table = 'permissions'
