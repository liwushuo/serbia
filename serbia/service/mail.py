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

    @staticmethod
    def send_vpn_bundle(email, bundle):
        title = u'企业 VPN 配置文件'
        body_tpl = u'文件见附件\n配置教程： https://shimo.im/docs/9IIUxN393gEVjAG2'
        msg = Message(title, recipients=[email], body=body_tpl)
        msg.attach('vpn_bundle.zip', 'application/zip', bundle.getvalue())
        mail.send(msg)
