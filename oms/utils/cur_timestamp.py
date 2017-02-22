#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import datetime


# get current time , use unix time
def cur_timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))
