#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from lib import config

# mysql connection pool
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


# base model
class BaseModel(Model):
    class Meta:
        database = db


# task table
class Task(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    creator = CharField()
    ip = CharField()
    create_time = IntegerField()
    target = CharField()
    version = IntegerField()
    type = CharField()
    content = CharField()
    description = CharField()
    executor = CharField()
    status = BooleanField()
    start_time = IntegerField()
    revert_time = IntegerField()
    percent = IntegerField()
    revert = BooleanField()

    class Meta:
        db_table = 'task'


# machine table
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


# user table
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


# session table
class Session(BaseModel):
    id = IntegerField()
    username = CharField(unique=True)
    access_token = CharField(unique=True)
    action_time = IntegerField()
    expire_time = IntegerField()

    class Meta:
        db_table = 'session'


# permissions table
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = CharField(unique=True)

    class Meta:
        db_table = 'permissions'
