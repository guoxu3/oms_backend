#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from dbbase import BaseModel
from ...lib.logger import log


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


# 获取machine_info信息
def get(machine_name=None, start=0, count=10):
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


# 插入数据到machine_info表
def add(machine_info_dict):
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


# 更新machine_info数据
def update(machine_info_dict):
    machine_info = MachineInfo.get(machine_name=machine_info_dict['machine_name'])
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
def delete(machine_name):
    delete = (MachineInfo
              .delete()
              .where(MachineInfo.machine_name == machine_name))
    try:
        delete.execute()
    except Exception, e:
        log.exception('exception')
        return False