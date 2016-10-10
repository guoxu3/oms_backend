#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config
import torndb

conn = torndb.Connection(
     host=config.dbhost, database=config.dbname,
     user=config.dbuser, password=config.dbpass )


# 查询task_id对应的信息
def select_task_id(task_id):

    return conn.get("select * from task_status where task_id=%s" % task_id)


# 插入task_id信息
def insert_task_data(task_id, data):
    sql = "INSERT INTO test (id,name,date) VALUES (%s,%s,%s)"
    conn.insert(sql, 100, "aaa", '0000-01-01')
    pass


# 更新task_id对应的数据
