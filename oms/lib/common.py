#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
   common functions
"""

import time
import datetime
from lib import config
from db import db_session


def unicode_to_str(_input):
    if isinstance(_input, dict):
        return {unicode_to_str(key): unicode_to_str(value) for key, value in _input.iteritems()}
    elif isinstance(_input, list):
        return [unicode_to_str(element) for element in _input]
    elif isinstance(_input, unicode):
        return _input.encode('utf-8')
    else:
        return _input


# get current time , use unix time
def cur_timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


# update user action time
def update_timestamp(access_token):
    session_data = {'access_token': access_token, 'action_time': cur_timestamp()}
    session_data['expire_time'] = session_data['action_time'] + config.expire_second
    db_session.update(session_data)
