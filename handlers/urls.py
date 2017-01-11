#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
collect all handlers
"""

from handlers import task,task_status,machine,update,user,login,permisson

# Routes
handlers = []
handlers.extend(task.handlers)
handlers.extend(task_status.handlers)
handlers.extend(machine.handlers)
handlers.extend(update.handlers)
handlers.extend(user.handlers)
handlers.extend(login.handlers)
handlers.extend(permisson.handlers)
