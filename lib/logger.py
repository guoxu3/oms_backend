#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time

print time.strftime('%H%M%S')

log_filename = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + "oms-" + time.strftime('%Y%m%d') + ".log"

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=log_filename,
                filemode='a')