#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
加密函数
"""

from random import Random
from hashlib import md5


def create_salt(salt_length=4):
    """
    随机生成指定长度的salt，用于和原始字符串组合，进行md5加密
    @param salt_length:  生成的salt值的长度
    @return:
    """

    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(salt_length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]

    return salt


def md5_salt(encrypt_str, salt=create_salt()):
    """
    @param encrypt_str:  要加密的字符串
    @param salt:  加盐的值
    @return: md5加密后的字符串
    """

    return md5(encrypt_str + salt).hexdigest()
