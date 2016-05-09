# -*- coding: utf-8 -*-

__all__ = ['db']

from raven.contrib.flask import Sentry
from flask_ldap import LDAP
from flask_mail import Mail
from serbia.extensions.flask_ldap_manage import FlaskLDAPManage

sentry = Sentry()
ldap = LDAP()
mail = Mail()
ldap_manage = FlaskLDAPManage()
