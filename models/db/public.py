#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 public database operation
"""

import db_session,db_user
from lib.common import *


# get username、expired_time and permissions
def get_info_by_token(access_token):
    info = db_session.get(access_token)
    info['permissions'] = db_user.get(info['username'])['permissions']
    return info


# update user actime and expired time
def update_expire_time(access_token):
    data = {'access_token': access_token, 'action_time': cur_timestamp(), 'expire_time': cur_timestamp() + config.expire_second}
    db_session.update(data)
