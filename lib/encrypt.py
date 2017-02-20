#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    encrypt functions
"""

from random import Random
from hashlib import md5
import uuid
import base64


def create_salt(salt_length=4):
    """
    Randomly generated specified length of salt
    @param salt_length:  length of salt value
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
    @param encrypt_str:  String needed to be encrypted
    @param salt:  salt value
    @return:  md5 encrypt string
    """
    return salt, md5(encrypt_str + salt).hexdigest()


# create cookie value
def make_cookie_secret():
    return base64.b64encode(
        uuid.uuid4().bytes + uuid.uuid4().bytes)


# base64 encrypt
def base64_encode(value):
    return base64.b16decode(value)
