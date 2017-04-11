#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    machine table operation
"""

from _db_init import *
from lib.logger import log


def row_count():
    try:
        count = Machine.select().count()
    except Exception:
        log.exception('exception')
        return 0
    else:
        return count


def get(machine_name=None, start=0, count=10):
    if machine_name:
        try:
            info = Machine.select().where(Machine.machine_name == machine_name).get()
        except Exception:
            log.exception('exception')
            return False
        else:
            return info.__dict__['_data']
    else:
        data_list = []
        try:
            for info in Machine.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception:
            log.exception('exception')
            return False
        else:
            return data_list


def add(machine_info_dict):
    machine = Machine()
    for key in machine_info_dict:
        setattr(machine, key, machine_info_dict[key])
    try:
        machine.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def update(machine_dict):
    machine = Machine.get(machine_name=machine_dict['machine_name'])
    for key in machine_dict:
        if key != 'machine_name':
            setattr(machine, key, machine_dict[key])
    try:
        machine.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def delete(machine_name):
    del_data = (Machine
                .delete()
                .where(Machine.machine_name == machine_name))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False


def update_initialize_status(ip=None, software=None, status=0):
    if ip:
        if software == 'init':
            query = Machine.update(is_initialized = status).where(Machine.inside_ip == ip)
        elif software in ['mysql', 'php', 'redis', 'nginx', 'memcached', 'jdk', 'tomcat']:
            query = Machine.update(software = status).where(Machine.inside_ip == ip)
        else:
            return False

        try:
            query.execute()
        except Exception:
            log.exception('exception')
        else:
            return True
    else:
        return False
