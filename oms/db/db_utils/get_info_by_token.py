#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db_session,db_user


# get username、expired_time and permissions
def get_info_by_token(access_token):
    info = db_session.get(access_token)
    info['permissions'] = db_user.get(info['username'])['permissions']
    return info
