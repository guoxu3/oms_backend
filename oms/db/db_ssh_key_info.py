#!/usr/bin/env python
# -*- coding:utf-8 -*-

from _db_init import *
from lib.logger import log


def add(ssh_key_dict):
    ssh_key_info = SshKeyInfo()
    for key in task_dict:
        setattr(ssh_key_info, key, ssh_key_dict[key])
    try:
        task.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def get(mode=None, username=None, ip=None):
    data_list = []
    if mode == 'ip':
        try:
            for info in SshKeyInfo.select().where(SshKeyInfo.ip == ip).get():
                data_list.append(info.__dict__['_data'])
        except Exception:
            log.exception('exception')
            return False
        else:
            return data_list
    elif mode == 'user':
        try:
            for info in SshKeyInfo.select().where(SshKeyInfo.username == username).get():
                data_list.append(info.__dict__['_data'])
        except Exception:
            log.exception('exception')
            return False
        else:
            return data_list
    else:
        return False


def delete(username, ip, system_user):
    del_data = (SshKeyInfo
                .delete()
                .where(
                    (SshKeyInfo.username == username) &
                    (SshKeyInfo.ip == ip) &
                    (SshKeyInfo.syytem_user == system_user)))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True
