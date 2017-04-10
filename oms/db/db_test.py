#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from playhouse.pool import PooledMySQLDatabase

# mysql connection pool
db = PooledMySQLDatabase(
    database='oms',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
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
    remarks = CharField()
    nginx = IntegerField()
    mysql = IntegerField()
    php = IntegerField()
    redis = IntegerField()
    memcache = IntegerField()
    jdk = IntegerField()
    tomcat = IntegerField()

    class Meta:
        db_table = 'machine'


# machine table
class SshKeyInfo(BaseModel):
    id = IntegerField()
    username = CharField()
    ip = CharField()
    system_user = CharField()

    class Meta:
        db_table = 'ssh_key_info'


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


# permissions table
class Permissions(BaseModel):
    id = IntegerField()
    permission = CharField(unique=True)
    permission_desc = CharField()
    permission_code = CharField(unique=True)

    class Meta:
        db_table = 'permissions'


def get_user_task_num_by_time(begin_time=0, end_time=0):
    user_list = []
    for a in User.select(User.username):
        user_list.append(a.__dict__['_data']['username'])
    user_task_statistic = {}
    query = (Task
             .select(Task.creator, fn.COUNT(Task.task_id).alias('task_sum'),
                     fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
             .where(
                    (Task.create_time >= begin_time) &
                    (Task.create_time <= end_time))
             .group_by(Task.creator, SQL('create_date')))
    try:
        for info in query.execute():
            creator = info.__dict__['_data']['creator']
            task_sum = info.__dict__['task_sum']
            create_date = info.__dict__['create_date']
            if create_date not in user_task_statistic:
                user_task_statistic[create_date] = {creator: task_sum}
            else:
                user_task_statistic[create_date][creator] = task_sum
        print user_task_statistic, user_list
    except Exception:

        return False
    else:
        return user_task_statistic, user_list


def get_permission(is_all=False, start=0, count=10):
    data_list = []
    if is_all:
        try:
            for info in Permissions.select():
                _data = info.__dict__['_data']
                permission_code = _data['permission_code']
                if len(permission_code) == 1:
                    pid = '0'
                else:
                    pid = '.'.join(permission_code.split('.')[:-1])

                name = _data['permission_desc'] + '[' + _data['permission'] + ']' + '[' + _data['permission_code'] + ']'
                permission_dcit = {
                    'id': permission_code,
                    'pId': pid,
                    'name': name
                }
                data_list.append(permission_dcit)
        except Exception:
            return False
        else:
            return data_list
    else:
        try:
            for info in Permissions.select().offset(start).limit(count):
                data_list.append(info.__dict__['_data'])
        except Exception:
            return False
        else:
            return data_list


def add(ssh_key_dict):
    ssh_key_info = SshKeyInfo()
    for key in ssh_key_dict:
        setattr(ssh_key_info, key, ssh_key_dict[key])
    try:
        ssh_key_info.save()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True


def get(mode=None, username=None, ip=None):
    data_list = []
    if mode == 'ip':
        print ip
        try:
            for info in SshKeyInfo.select().where(SshKeyInfo.ip == ip):
                data = info.__dict__['_data']
                data_list.append({data['username']: data['system_user']})
        except Exception, e:
            print e
            return False
        else:
            return data_list
    elif mode == 'user':
        try:
            for info in SshKeyInfo.select().where(SshKeyInfo.username == username):
                data = info.__dict__['_data']
                data_list.append({data['ip']: data['system_user']})
        except Exception, e:
            print e
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
                    (SshKeyInfo.system_user == system_user)))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        return True

"""
print add({'username': 'guoxu', 'ip': '192.168.1.1', 'system_user': 'root'})
print add({'username': 'guoxu', 'ip': '192.168.1.1', 'system_user': 'admin'})
print add({'username': 'guoxu', 'ip': '192.168.1.2', 'system_user': 'root'})
print add({'username': 'guoxu', 'ip': '192.168.1.3', 'system_user': 'root'})
print add({'username': 'guoxu', 'ip': '192.168.1.4', 'system_user': 'root'})
print add({'username': 'guoxu', 'ip': '192.168.1.4', 'system_user': 'admin'})
print add({'username': 'guoxu', 'ip': '192.168.1.5', 'system_user': 'root'})
"""

print get('ip', '', '192.168.1.4')
