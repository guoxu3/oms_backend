#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
read the config file
"""

import os
import ConfigParser
import re


# get config file
def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/conf/oms_test.conf'
    config.read(path)
    return config.get(section, key)

# database config
dbhost = get_config("database", "dbhost")
dbport = int(get_config("database", "dbport"))
dbuser = get_config("database", "dbuser")
dbpass = get_config("database", "dbpass")
dbname = get_config("database", "dbname")

# server config
port = get_config("server", "port")
address = get_config("server", "address")

# session config
# default expiration time 7200s
exp_second = 7200
# get config
exp_time = get_config("session", "exp_time")
if re.match("^[0-9]*h$", exp_time):
    exp_second = int(exp_time.replace('h','')) * 3600
elif re.match("^[0-9]*m$", exp_time):
    exp_second = int(exp_time.replace('m','')) * 60
elif re.match("^[0-9]*s$", exp_time):
    exp_second = int(exp_time.replace('s',''))
