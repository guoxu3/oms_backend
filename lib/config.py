#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
read the config file
"""

import os
import ConfigParser


# get config file
def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/conf/oms.conf'
    config.read(path)
    return config.get(section, key)

# database config
dbhost = get_config("database", "dbhost")
dbport = get_config("database", "dbport")
dbuser = get_config("database", "dbuser")
dbpass = get_config("database", "dbpass")
dbname = get_config("database", "dbname")

# server config
port = get_config("server", "port")
listen = get_config("server", "listen")