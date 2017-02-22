#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import verify


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
