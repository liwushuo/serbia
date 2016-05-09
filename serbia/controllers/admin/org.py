# -*- coding: utf-8 -*-

from flask import render_template

from serbia.core import ldap_manage
from serbia.utils.auth import admin_auth_required
from . import bp


@bp.route('/orgs')
@admin_auth_required
def list_orgs():
    orgs = ldap_manage.client.list_orgs()
    return render_template('admin/org/list.html', orgs=orgs)
