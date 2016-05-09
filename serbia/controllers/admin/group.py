# -*- coding: utf-8 -*-

from flask import render_template

from serbia.core import ldap_manage
from serbia.utils.auth import admin_auth_required
from . import bp


@bp.route('/groups')
@admin_auth_required
def list_groups():
    groups = ldap_manage.client.list_groups()
    return render_template('admin/group/list.html', groups=groups)
