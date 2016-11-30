#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    == 验证类 ==
"""

import types
import re
import time
import httplib
import urllib
import base64
import uuid
import markdown2
import json


class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


# 判断是否为整数 15
def is_number(value):
    # if False == type(value) is int:
    # return str(value).isdigtal()
    # return False
    # return True
    return str(value).isdigit()


# 判断是否为字符串 string
def is_string(value):
    return isinstance(value, bytes)


# 判断是否为浮点数 1.324
def is_float(value):
    return isinstance(value, float)


# 判断是否为字典 {'a1':'1','a2':'2'}
def is_dict(value):
    return isinstance(value, dict)


# 判断是否为tuple [1,2,3]
def is_tuple(value):
    return isinstance(value, tuple)


# 判断是否为List [1,3,4]
def is_list(value):
    return isinstance(value, list)


# 判断是否为布尔值 True
def is_boolean(value):
    return isinstance(value, bool)


# 判断是否为货币型 1.32
def is_currency(value):
    # 数字是否为整数或浮点数
    if is_float(value) and is_number(value) and value > 0:
        # 数字不能为负数
        # return is_number(currencyObj)
        return False
    return True


# 判断某个变量是否为空 x
def is_empty(value):
    if len(value) == 0:
        return True
    return False


# 不为空
def not_empty(value):
    if is_none(value):
        return False
    if is_empty(value):
        return False
    return True


# 判断变量是否为None None
def is_none(value):
    return isinstance(value, type(None))  # == "None" or value == "none":


# 判断是否为日期格式,并且是否符合日历规则 2010-01-31
def is_date(value):
    if len(value) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match(rule, value)
        if match:
            return True
        return False
    return False


# 判断是否为邮件地址
def is_email(value):
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match(rule, value)

    if match:
        return True
    return False


# 判断是否为中文字符串
def is_chinese_char_string(value):
    for x in value:
        if (x >= u"\u4e00" and x <= u"\u9fa5") or (x >= u'\u0041' and x <= u'\u005a') or (
                        x >= u'\u0061' and x <= u'\u007a'):
            continue
        else:
            return False
    return True


# 判断是否为中文字符
def is_chinese_char(value):
    if value[0] > chr(127):
        return True
    return False


# 判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
def is_legala_ccounts(value):
    rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
    match = re.match(rule, value)

    if match:
        return True
    return False


# 匹配IP地址
def is_ip_addr(value):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, value):
        return False
    else:
        return True


# 判断是否是json
def is_json(value):
    try:
        json.loads(value)
    except ValueError:
        return False
    return True


# 判断content-type 是不是application/json;charset=utf8
def is_content_type_right(value):
    value = str.lower(value.replace(" ", ""))
    type = value.split(";")[0]
    charset = value.split(";")[1].split("=")[1].replace("-", "")
    if type == "application/json" and charset == "utf8":
        return True
    return False


def regex(pattern, data, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def ip(data):
    pattern = r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'
    return regex(pattern, data, re.IGNORECASE)


def xmldatetime(value):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)))


def xmldatetimeym(value):
    return time.strftime('%Y-%m', time.localtime(int(value)))


def xmldatetimeymd(value):
    return time.strftime('%Y-%m-%d', time.localtime(int(value)))


def xmldatetimey(value):
    return time.strftime('%Y', time.localtime(int(value)))


def xmldatetimed(value):
    return time.strftime('%d', time.localtime(int(value)))


def xmldatetimem(value):
    return time.strftime('%m', time.localtime(int(value)))


def get_api_data(url, project, password, value):
    headers = {"User-Agent": 'curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 '
                             'NSS/3.13.1.0 zlib/1.2.3 libidn/1.18 libssh2/1.2.2',
               "Host": 'portal.4399.com',
               "Accept": "*/*",
               "Proxy-Connection": "Keep-Alive",
               "Content-Type": "application/x-www-form-urlencoded"}

    params = urllib.urlencode({"password": password, "method": value})
    try:
        conn = httplib.HTTPConnection(url, 80, timeout=2)
        conn.request("POST", "/api/{0}/get_api.php".format(project), body=params, headers=headers)
        response = conn.getresponse().read()
        response = [info for info in response.split('\n') if re.match('^(\w)', info)]
        return response
    except Exception, e:
        return False


byte_map = ('B', 'KB', 'MB', 'GB', 'TB')


def size_readify(size, precise=1):
    """do this kind of things:
    1024 => 1 KB"""
    level = 0
    while size >= 1024:
        size = size / 1024.0
        level += 1
    return str(round(size, precise)) + ' ' + byte_map[level]


def markdownhtml(text):
    return markdown2.markdown(text, extras=["wiki-tables", "code-color", "fenced-code-blocks"])
