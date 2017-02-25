#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import verify


def check_machine_input(machine_dict):
    """
        check machine input info format
        @parm user_dict: Dictionary, an machine info dictionary
        @return ok: Boolean , info check pass or not
        @return info: String, message return to user
    """
    ok = True
    info = ""

    if 'inside_ip' in machine_dict and not verify.is_ip_addr(machine_dict['inside_ip']):
        ok = False
        info = 'Inside ip format error'
        return ok, info

    if 'outside_ip' in machine_dict and not verify.is_ip_addr(machine_dict['outside_ip']):
        ok = False
        info = 'Outside ip format error'
        return ok, info

    if 'is_initialized' in machine_dict and not verify.is_boolean(machine_dict['is_initialized']):
        ok = False
        info = 'Initialized info format error'
        return ok, info

    return ok, info
