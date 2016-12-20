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
