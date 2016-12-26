#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 定义machine表的相关操作
"""

from peewee import *
from _db_init import *
from lib.logger import log


# 获取总数量
def row_count():
    try:
        count = Machine.select().count()
    except Exception, e:
        log.exception('exception')
        return 0
    else:
        return count


# 获取machine_info信息
def get(machine_name=None, start=0, count=10):
    if machine_name:
        try:
            info = Machine.select().where(Machine.machine_name == machine_name).get()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in Machine.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return data_list


# 插入数据到machine_info表
def add(machine_info_dict):
    machine = Machine()
    for key in machine_info_dict:
        setattr(machine, key, machine_info_dict[key])
    try:
        machine.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 更新machine_info数据
def update(machine_dict):
    machine = Machine.get(machine_name=machine_dict['machine_name'])
    for key in machine_dict:
        if key != 'machine_name':
            setattr(machine, key, machine_dict[key])
    try:
        machine.save()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return True


# 删除machine_info数据
def delete(machine_name):
    del_data = (Machine
                .delete()
                .where(Machine.machine_name == machine_name))
    try:
        del_data.execute()
    except Exception, e:
        log.exception('exception')
        return False
