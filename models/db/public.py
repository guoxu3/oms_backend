#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 public database operation
"""

import db_session,db_user
from lib import common, config


# get username、expired_time and permissions
def get_info_by_token(access_token):
    info = db_session.get(access_token)
    info['permissions'] = db_user.get(info['username'])['permissions']
    return info


# update user actime and expired time
def update_expire_time(access_token):
    action_time = common.cur_timestamp()
    data = {'access_token': access_token, 'action_time': action_time, 'expire_time': action_time + config.expire_second}
    db_session.update(data)
