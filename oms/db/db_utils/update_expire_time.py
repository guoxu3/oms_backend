#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db import db_session
from lib import config
import utils


# update user action time and expired time
def update_expire_time(access_token):
    action_time = utils.cur_timestamp()
    data = {'access_token': access_token, 'action_time': action_time, 'expire_time': action_time + config.expire_second}
    db_session.update(data)
