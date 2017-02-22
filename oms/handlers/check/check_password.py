#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import encrypt
from db import db_user


def check_password(username, imput_passwd):
    ok = True
    info = ""
    saved_user_data = db_user.get(username)
    if not saved_user_data:
        ok = False
        info = "No such a user"
    else:
        saved_salt = saved_user_data['salt']
        saved_passwd = saved_user_data['passwd']
        _, encrypt_passwd = encrypt.md5_salt(imput_passwd, saved_salt)
        if saved_passwd != encrypt_passwd:
            ok = False
            info = "Password auth failed"
    return ok, info
