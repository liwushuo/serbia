# -*- coding: utf-8 -*-

from flask import current_app
from flask import render_template_string
from flask import url_for
from flask_mail import Message

from serbia.core import mail


class MailService(object):

    @staticmethod
    def send_reset_password(email, url):
        title = u'重置密码'
        body_tpl = u'重置链接：%s' % url
        msg = Message(title, recipients=[email], body=body_tpl)
        mail.send(msg)
