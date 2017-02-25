#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import verify


def check_user_input(user_dict):
    """
        check user input info format
        @parm user_dict: Dictionary, an user info dictionary
        @return ok: Boolean , info check pass or not
        @return info: String, message return to user
    """
    ok = True
    info = ""
    if 'mail' in user_dict and not verify.is_mail(user_dict['mail']):
        ok = False
        info = 'E-mail format error'
        return ok, info

    if 'passwd' in user_dict and not verify.is_password(user_dict['passwd']):
        ok = False
        info = 'Password format error'
        return ok, info

    if 'old_passwd' in user_dict and not verify.is_password(user_dict['old_passwd']):
        ok = False
        info = 'Old password format error'
        return ok, info

    if 'new_passwd' in user_dict and not verify.is_password(user_dict['new_passwd']):
        ok = False
        info = 'New password format error'
        return ok, info

    if 'username' in user_dict and not verify.is_legal_accounts(user_dict['username']):
        ok = False
        info = 'Username format error'
        return ok, info

    return ok, info
