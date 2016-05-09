# -*- coding: utf-8 -*-

import ldap
import ldap.modlist as modlist
import base64
import sha

from flask import _app_ctx_stack as stack
from flask import current_app

class _LDAPUser(object):

    def __init__(self, user_dict):
        self._user_dn = user_dict[0]
        self._user_attrs = user_dict[1]

    def _get_user_dn(self):
        return self._user_dn
    dn = property(_get_user_dn)

    def _get_user_attrs(self):
        return self._user_attrs
    attrs = property(_get_user_attrs)

    # def _get_user_uid(self):
    #     return self._user_attrs['uid'][0]
    # uid = property(_get_user_uid)

    @property
    def uid(self):
        return self._user_attrs['uid'][0]

    @property
    def mail(self):
        return self._user_attrs['mail'][0]

    @property
    def displayName(self):
        return self._user_attrs['displayName'][0].decode('utf-8')

    @property
    def uidNumber(self):
        return self._user_attrs['uidNumber'][0]

    @property
    def ou(self):
        return self._user_dn.split(',', 2)[1].split('=')[1]


class _LDAPGroup(object):

    def __init__(self, group_dict):
        self._group_dn = group_dict[0]
        self._group_attrs = group_dict[1]

        self._name = self._url = None
        description = group_dict[1].get('description')
        if description:
            field_len = len(description.split(','))
            if field_len == 2:
                self._name, self._url = description.split(',')
            else:
                self._name = description


    def _get_group_dn(self):
        return self._group_dn
    dn = property(_get_group_dn)

    def _get_group_attrs(self):
        return self._group_attrs
    attrs = property(_get_group_attrs)

    def _get_group_cn(self):
        return self._group_attrs['cn'][0]
    cn = property(_get_group_cn)

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url



class _LDAPOrg(object):

    def __init__(self, org_dict):
        self._org_dn = org_dict[0]
        self._org_attrs = org_dict[1]

    def _get_org_dn(self):
        return self._org_dn
    dn = property(_get_org_dn)

    def _get_org_attrs(self):
        return self._org_attrs
    attrs = property(_get_org_attrs)

    @property
    def description(self):
        return self._org_attrs['description'][0]

    @property
    def ou(self):
        return self._org_dn.split(',', 1)[0].split('=')[1]


class LDAPManage(object):
    def __init__(self, settings):
        self.con = ldap.initialize(settings['LDAP_URI'])
        self.base_dn = settings['LDAP_BASE_DN']
        self.user_ou = settings['LDAP_USER_OU']
        self.group_ou = settings['LDAP_GROUP_OU']
        self.archive_ou = settings['LDAP_ARCHIVE_OU']
        self.con.simple_bind_s(settings['LDAP_ADMIN_USER'], settings['LDAP_ADMIN_PASSWORD'])

    def unbind(self):
        self.con.unbind_s()

    def get_user(self, uid):
        ldap_filter = '(&(objectclass=posixAccount)(uid=%s))' % uid
        records = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        if records:
            return _LDAPUser(records[0])

    def get_user_by_email(self, email):
        print email
        ldap_filter = '(&(objectclass=posixAccount)(mail=%s))' % email
        records = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        if records:
            return _LDAPUser(records[0])

    def get_group(self, group_name):
        ldap_filter = '(&(objectclass=posixGroup)(cn=%s))' % group_name
        records = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        if records:
            return _LDAPGroup(records[0])

    def _get_next_uid(self):
        ldap_filter = '(objectClass=posixAccount)'
        users = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        uids = [int(user[1]['uidNumber'][0]) for user in users]
        return max(uids) + 1

    def _get_next_gid(self):
        ldap_filter = '(objectClass=posixGroup)'
        groups = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        gids = [int(group[1]['gidNumber'][0]) for group in groups]
        return max(gids) + 1

    def list_users(self):
        ldap_filter = '(objectClass=posixAccount)'
        users = self.con.search_s(self.user_ou, ldap.SCOPE_SUBTREE, ldap_filter)
        return [_LDAPUser(user) for user in users]

    def list_groups(self):
        ldap_filter = '(objectClass=posixGroup)'
        groups = self.con.search_s(self.group_ou, ldap.SCOPE_SUBTREE, ldap_filter)
        return [_LDAPGroup(group) for group in groups]

    def list_orgs(self):
        ldap_filter = '(&(!(ou=people))(objectClass=organizationalUnit))'
        orgs = self.con.search_s(self.user_ou, ldap.SCOPE_SUBTREE, ldap_filter)
        return [_LDAPOrg(org) for org in orgs]

    def list_users_by_group(self, group_name):
        group = self.get_group(group_name)
        if not group:
            return []
        uids = group.attrs.get('memberUid', [])
        return [self.get_user(uid) for uid in uids]

    def list_users_by_org(self, org_ou):
        org_dn = 'ou=%s,%s' % (org_ou, self.user_ou)
        ldap_filter = '(objectClass=posixAccount)'
        users = self.con.search_s(org_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        return [_LDAPUser(user) for user in users]

    def list_user_groups(self, uid):
        ldap_filter = '(&(cn=*)(memberUid=%s))' % uid
        groups = self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, ldap_filter)
        return [_LDAPGroup(group) for group in groups]

    def remove_user_from_group(self, uid, group_name):
        group_dn = self.get_group(group_name).dn
        mod_attrs = [
            (ldap.MOD_DELETE, 'memberUid', uid),
        ]
        try:
            self.con.modify_s(group_dn, mod_attrs)
        except ldap.NO_SUCH_ATTRIBUTE:
            pass

    def add_user_to_group(self, uid, group_name):
        group_dn = self.get_group(group_name).dn
        mod_attrs = [
            (ldap.MOD_ADD, 'memberUid', uid),
        ]
        try:
            self.con.modify_s(group_dn, mod_attrs)
        except ldap.TYPE_OR_VALUE_EXISTS:
            pass

    def add_users_to_group(self, uids, group_name):
        for uid in uids:
            self.add_user_to_group(uid, group_name)

    def remove_users_from_group(self, uids, group_name):
        for uid in uids:
            self.remove_user_from_group(uid, group_name)

    def add_user_to_groups(self, uid, group_names):
        for group_name in group_names:
            self.add_user_to_group(uid, group_name)

    def remove_user_from_groups(self, uid, group_names):
        for group_name in group_names:
            self.remove_user_from_group(uid, group_name)

    def remove_user_from_all_group(self, uid):
        groups = self.list_user_groups(uid)
        for group in groups:
            self.remove_user_from_group(uid, group.cn)

    def update_user_org(self, uid, new_ou):
        org_dn = 'ou=%s,%s' % (new_ou, self.user_ou)
        user_dn = self.get_user(uid).dn
        self.con.rename_s(user_dn, user_dn.split(',', 1)[0], org_dn)

    def encrypt_pass(self, password):
        return "{SHA}" + base64.encodestring(sha.new(str(password)).digest())

    def update_user_password(self, uid, new_password):
        user_dn = self.get_user(uid).dn
        encrypted_pass = self.encrypt_pass(new_password)
        mod_attrs = [
            (ldap.MOD_REPLACE, 'userPassword', encrypted_pass),
        ]
        self.con.modify_s(user_dn, mod_attrs)

    def add_user(self, displayName, sn, givenName, uid, password, mail, cn, org):
        org_dn = 'ou=%s,%s' % (org, self.user_ou)
        user_dn = 'cn=%s,%s' % (cn, org_dn)

        attrs = {
            'displayName': displayName,
            'uid': uid,
            'objectClass': ['inetOrgPerson', 'posixAccount', 'top'],
            'userPassword': self.encrypt_pass(password),
            'gidNumber': '0',
            'sn': sn,
            'homeDirectory': '/home/users/%s' % uid,
            'mail': mail,
            'givenName': givenName,
            'uidNumber': str(self._get_next_uid()),
            'cn': cn
        }
        self.add(user_dn, attrs)

    def add_group(self, cn, name, url):
        group_dn = 'cn=%s,%s' % (cn, self.group_ou)
        if url:
            name = name + ',' + url
        attrs = {
            'objectClass': ['posixGroup', 'top'],
            'memberUid': [],
            'gidNumber': str(self._get_next_gid()),
            'cn': cn,
            'description': name,
        }
        self.add(group_dn, attrs)

    def add(self, dn, attrs):
        mod_attrs = modlist.addModlist(attrs)
        self.con.add_s(dn, mod_attrs)

    def archive_user(self, uid):
        user_dn = self.get_user(uid).dn
        self.remove_user_from_all_group(uid)
        self.con.rename_s(user_dn, user_dn.split(',', 1)[0], self.archive_ou)

    def delete_user(self, uid):
        user_dn = self.get_user(uid).dn
        self.remove_user_from_all_group(uid)
        self.delete(user_dn)

    def delete_group(self, group_name):
        group_dn = self.get_group(group_name).dn
        self.delete(group_dn)

    def delete(self, dn):
        self.con.delete_s(dn)


class FlaskLDAPManage(object):

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def connect(self):
        return LDAPManage(current_app.config)
        # con = ldap.initialize(self.settings['LDAP_URI'])
        # return con.simple_bind_s(self.settings['LDAP_ADMIN_USER'], self.settings['LDAP_ADMIN_PASSWORD'])

    def teardown(self):
        ctx = stack.top
        if hasattr(ctx, 'ldap_manage'):
            ctx.ldap_manage.unbind_s()

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'ldap_manage'):
                ctx.ldap_manage = self.connect()
            return ctx.ldap_manage
