#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import verify


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
        info = 'Request body format error'
    return ok, info
