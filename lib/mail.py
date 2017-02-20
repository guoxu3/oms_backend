#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    using to send systemg notification
"""

import smtplib
from email.mime.text import MIMEText
from logger import log
import config


def send_mail(mailto_list, message):
    if config.mail_open == "True":
        mail_host = config.mail_host
        mail_user = config.mail_user
        mail_pass = config.mail_pass
        mail_postfix = config.mail_postfix

        msg = MIMEText(message, 'plain')
        msg['From'] = mail_user + '@' + mail_postfix
        msg['Subject'] = 'XXX OMS Notification'
        msg['To'] = ",".join(mailto_list)

        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user, mail_pass)
            server.sendmail(msg['From'], mailto_list, msg.as_string())
            server.close()
        except Exception, e:
            log.exception('exception')
        else:
            log.info("sending mail successful.")
    else:
        pass

