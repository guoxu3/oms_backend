#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    judge funtions
"""

import re
import json
import utils
from db import db_session
from lib import config
from db import db_utils


class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def is_number(value):
    # if False == type(value) is int:
    # return str(value).isdigtal()
    # return False
    # return True
    return str(value).isdigit()


def is_string(value):
    return isinstance(value, bytes)


def is_float(value):
    return isinstance(value, float)


def is_dict(value):
    return isinstance(value, dict)


def is_tuple(value):
    return isinstance(value, tuple)


def is_list(value):
    return isinstance(value, list)


def is_boolean(value):
    return isinstance(value, bool)


def is_empty(value):
    if len(value) == 0:
        return True
    return False


def not_empty(value):
    if is_none(value):
        return False
    if is_empty(value):
        return False
    return True


def is_none(value):
    return isinstance(value, type(None))  # == "None" or value == "none":


# date format: 2010-01-31
def is_date(value):
    if len(value) == 10:
        rule = "(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-" \
               "(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|" \
               "(02-(0[1-9]|[1][0-9]|2[0-8]))))" \
               "|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/"
        match = re.match(rule, value)
        if match:
            return True
        return False
    return False


def is_email(value):
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match(rule, value)

    if match:
        return True
    return False


def is_chinese_char_string(value):
    for x in value:
        if (x >= u"\u4e00" and x <= u"\u9fa5") or (x >= u'\u0041' and x <= u'\u005a') or \
                ( x >= u'\u0061' and x <= u'\u007a'):
            continue
        else:
            return False
    return True


def is_chinese_char(value):
    if value[0] > chr(127):
        return True
    return False


# 4-16 byters, allowed alphanumeric characters and underscores
# must begin with characters
def is_legal_accounts(value):
    rule = '[a-zA-Z0-9_]{3,15}$'
    match = re.match(rule, value)

    if match:
        return True
    return False


def is_password(value):
    rule = '[a-zA-Z0-9_!@#%^&*()]{6,20}$'
    match = re.match(rule, value)

    if match:
        return True
    return False


def is_ip_addr(value):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\b"
    if re.match(pattern, value):
        return True
    else:
        return True


def is_json(value):
    try:
        json.loads(value)
    except ValueError:
        return False
    return True


# content-type must be "application/json;charset=utf8"
def is_content_type_right(data):
    data = str.lower(data.replace(" ", ""))
    content_type = data.split(";")[0]
    charset = data.split(";")[1].split("=")[1].replace("-", "")
    if content_type == "application/json" and charset == "utf8":
        return True
    return False


def has_permission(access_token, local_permission_list):
    """
        verify if user has permisson
        @param access_token:  user's access_token, get form cookie
        @param local_permission_list:  function permission list
        @return ok: Boolean, has permission or not
        @return info: String , info return to user
        @return is_admin: Boolean
    """

    ok = False
    info = "No permission"
    is_admin = False
    permission_list = []
    user_info = db_utils.get_info_by_token(access_token)
    for a in user_info['permissions'].split(','):
        permission_list.append(a)
    # '0' represent administrator
    if '0' in permission_list:
        ok = True
        info = ""
        is_admin = True
    if set(permission_list) & set(local_permission_list) != set([]):
        ok = True
        info = ""

    return ok, info, is_admin


def is_expired(access_token):
    """
        verify if user has action time
        @param access_token:  user's access_token, get form cookie
        @return  Boolean, expired or not

    """
    info = db_utils.get_info_by_token(access_token)
    expire_time = info['expire_time']
    if utils.cur_timestamp() > expire_time:
        return True
    else:
        action_time = utils.cur_timestamp()
        session_data = {'username': info['username'], 'action_time': action_time,
                        'expire_time': action_time + config.expire_second }
        db_session.update(session_data)
        return False
