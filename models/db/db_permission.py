#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from dbbase import BaseModel
from ...lib.logger import log


# 定义权限表Permissions
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = IntegerField()

    class Meta:
        db_table = 'permissions'
