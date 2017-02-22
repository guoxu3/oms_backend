#!/usr/bin/env python
# -*- coding:utf-8 -*-


def unicode_to_str(_input):
    if isinstance(_input, dict):
        return {unicode_to_str(key): unicode_to_str(value) for key, value in _input.iteritems()}
    elif isinstance(_input, list):
        return [unicode_to_str(element) for element in _input]
    elif isinstance(_input, unicode):
        return _input.encode('utf-8')
    else:
        return _input
