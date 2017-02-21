#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import verify, encrypt
from models.db import db_user


def check_login(token):
    if token:
        if verify.is_expired(token):
            ok = False
            info = "Login timeout"
        else:
            ok = True
            info = ""
    else:
        ok = False
        info = "Please login first"
    return ok, info


def check_content_type(request):
    ok = True
    info = ""
    content_type = dict(request.headers)['Content-Type']
    body = request.body
    if not verify.is_content_type_right(content_type):
        ok = False
        info = "Request content-type format error"
    if not verify.is_json(body):
        ok = False
        info = 'Request content-type format error'
    return ok, info


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
