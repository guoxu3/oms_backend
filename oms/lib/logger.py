#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time
import os

root_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
log_filename = root_path + "/log/" + "oms-" + time.strftime('%Y%m%d') + ".log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_filename,
                    filemode='a')

log = logging.getLogger('root')
