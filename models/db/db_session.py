#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    session table operation
"""


from peewee import *
from _db_init import *
from lib.logger import log


def get(access_token):
    try:
        info = Session.select().where(Session.access_token == access_token).get()
    except Exception, e:
        log.exception('exception')
        return False
    else:
        return info.__dict__['_data']


# update session
# if username dosnot exist, add a new session record
def update(session_dict):
    try:
        session = Session.get(username=session_dict['username'])
    except Exception:
        log.exception('exception')
        session = Session()
        for key in session_dict:
            setattr(session, key, session_dict[key])
        try:
            session.save()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return True
    else:
        for key in session_dict:
            if key != 'username':
                setattr(session, key, session_dict[key])
        try:
            session.save()
        except Exception, e:
            log.exception('exception')
            return False
        else:
            return True


def delete(access_token):
    del_data = (Session
                .delete()
                .where(Session.access_token == access_token))
    try:
        del_data.execute()
    except Exception:
        log.exception('exception')
        return False
    else:
        if get(access_token):
            return False
        else:
            return True
