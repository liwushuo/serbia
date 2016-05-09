# -*- coding: utf-8 -*-

from .base import *


ENV = 'development'
DEBUG = True


# App Config
RESET_PASSWORD_TOKEN = 'dsf*@#eRID'
SITE_NAME = u'权限管理后台'

# LDAP AUTH
LDAP_LOGIN_ENABLE = True
LDAP_ADMIN_GROUP = ['ss-admin']
LDAP_AUTH_REQUIRE_GROUP = ['ss-user', 'ss-admin']
LDAP_USERS =  {
    'test': (
        'cn=test,ou=people,dc=ldap,dc=liwushuo,dc=com',
        {
            'uid': ['test'],
            'password': ['test'],
            'mail': ['test@liwushuo.com'],
            'uidNumber': ['1000'],
            'displayName': [u'编辑天尊'],
        }
    ),
    'maple': (
        'cn=maple,ou=people,dc=ldap,dc=liwushuo,dc=com',
        {
            'uid': ['maple'],
            'password': ['test'],
            'mail': ['admin@liwushuo.com'],
            'uidNumber': ['1031'],
            'displayName': [u'江湖骗子'],
        }
    )
}
LDAP_GROUPS = {
    'ss-user': (
        'cn=ss-users,ou=groups,dc=ldap,dc=liwushuo,dc=com',
        {
            'cn': ['ss-users'],
            'memberUid': ['test', 'maple'],
        }
    ),
    'ss-admin': (
        'cn=ss-admin,ou=groups,dc=ldap,dc=liwushuo,dc=com',
        {
            'cn': ['ss-admin'],
            'memberUid': ['maple'],
        }
    )
}

try:
    from .local import *
except ImportError as e:
    pass
