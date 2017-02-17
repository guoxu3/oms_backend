#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
    read the config file ,parse config
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
expire_second = 7200 # default expiration time 7200s
expire_time = get_config("session", "expire_time")
if re.match("^[0-9]*h$", expire_time):
    expire_second = int(expire_time.replace('h','')) * 3600
elif re.match("^[0-9]*m$", expire_time):
    expire_second = int(expire_time.replace('m','')) * 60
elif re.match("^[0-9]*s$", expire_time):
    expire_second = int(expire_time.replace('s',''))

# mail config
mail_open = get_config("mail", "mail_open")
mail_host = get_config("mail", "mail_host")
mail_user = get_config("mail", "mail_user")
mail_pass = get_config("mail", "mail_pass")
mail_postfix = get_config("mail", "mail_postfix")