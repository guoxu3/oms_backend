#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
   collect all handlers
"""

from handlers import task, machine, update, user, login, logout, permission

# Routes
handlers = []
handlers.extend(task.handlers)
handlers.extend(machine.handlers)
handlers.extend(update.handlers)
handlers.extend(user.handlers)
handlers.extend(login.handlers)
handlers.extend(permission.handlers)
handlers.extend(logout.handlers)
