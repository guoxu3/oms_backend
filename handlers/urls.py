#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
collect all handlers
"""

from handlers import api

# Routes
handlers = []
handlers.extend(api.handlers)

