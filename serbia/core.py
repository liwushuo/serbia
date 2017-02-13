# -*- coding: utf-8 -*-

__all__ = ['db']

from raven.contrib.flask import Sentry
from flask_ldap import LDAP
from flask_mail import Mail
from serbia.extensions.flask_ldap_manage import FlaskLDAPManage
from serbia.extensions.exmail import Exmail

sentry = Sentry()
ldap = LDAP()
mail = Mail()
ldap_manage = FlaskLDAPManage()
exmail = Exmail('liwushuo', 'b2cae7286afb59d06ea768c352c69a5c')
