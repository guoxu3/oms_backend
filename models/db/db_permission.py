#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义permission表的相关操作
"""

from peewee import *
from _db_conn import BaseModel


# 定义权限表Permissions
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = IntegerField()

    class Meta:
        db_table = 'permissions'
