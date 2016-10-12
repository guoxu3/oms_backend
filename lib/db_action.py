#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config
import torndb

def connection():
    conn = torndb.Connection(
        host=config.dbhost, database=config.dbname,
        user=config.dbuser, password=config.dbpass )
    return conn


# 查询task_id对应的信息
def select_from_task(task_id):
    conn = connection()
    sql = 'SELECT * FROM task WHERE task_id = %s'
    return  conn.get(sql, task_id)


# 插入task_id信息
def insert_task(data):
    conn = connection()
    sql = "INSERT INTO task (task_id,ip,action,content,description) VALUES (%s,%s,%s,%s,%s)"
    try:
        conn.insertmany(sql, [data])
    except:
        return 'failed'
    else:
        task_id = data[0]
        return  insert_task_status(task_id)


# 更新task_status表
def insert_task_status(task_id):
    conn = connection()
    sql = "INSERT INTO task_status (task_id) VALUES (%s)"
    try:
        conn.insert(sql, task_id)
    except:
        return 'failed'
    else:
        return 'success'


# 查询task_id对应的状态
def select_from_task_status(task_id):
    conn = connection()
    sql = 'SELECT * FROM task_status WHERE task_id = %s'
    return  conn.get(sql, task_id)


# 更新task_status
def update_task_status(task_id, percent):
    conn = connection()
    sql = "update task_status set status = 1,percent = %d where task_id = '%s'" % (percent, task_id)
    try:
        conn.execute(sql)
    except Exception, e:
        print e
        return False
    else:
        return True

