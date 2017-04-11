#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
   collect all handlers
"""

from handlers import task, machine, update, user, login, logout, permission, task_statistic, task_status
from handlers import ssh_key_manage, initialize

# Routes
handlers = []
handlers.extend(task.handlers)
handlers.extend(machine.handlers)
handlers.extend(update.handlers)
handlers.extend(user.handlers)
handlers.extend(login.handlers)
handlers.extend(permission.handlers)
handlers.extend(logout.handlers)
handlers.extend(task_statistic.handlers)
handlers.extend(task_status.handlers)
handlers.extend(ssh_key_manage.handlers)
handlers.extend(initialize.handlers)
