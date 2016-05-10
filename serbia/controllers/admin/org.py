# -*- coding: utf-8 -*-

import ldap
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from serbia.core import ldap_manage
from serbia.utils.auth import admin_auth_required
from . import bp


@bp.route('/orgs')
@admin_auth_required
def list_orgs():
    orgs = ldap_manage.client.list_orgs()
    return render_template('admin/org/list.html', orgs=orgs)


@bp.route('/orgs/add', methods=['GET', 'POST'])
@admin_auth_required
def add_org():
    if request.method == 'GET':
        return render_template('admin/org/add.html')

    ou = request.form.get('ou')
    name = request.form.get('name')
    ldap_manage.client.add_org(ou.encode('utf-8'), name.encode('utf-8'))
    flash(u'部门添加成功', 'success')
    return redirect(url_for('admin.list_orgs'))


@bp.route('/orgs/<org_ou>/update', methods=['GET', 'POST'])
@admin_auth_required
def update_org(org_ou):
    if request.method == 'GET':
        org = ldap_manage.client.get_org(org_ou)
        print org._org_attrs
        return render_template('admin/org/update.html', org=org)

    name = request.form.get('name')
    ldap_manage.client.update_org(org_ou.encode('utf-8'), name.encode('utf-8'))
    flash(u'部门信息更新成功', 'success')
    return redirect(request.referrer)


@bp.route('/orgs/<org_ou>/delete', methods=['POST'])
@admin_auth_required
def delete_org(org_ou):
    try:
        ldap_manage.client.delete_org(org_ou)
    except ldap.NOT_ALLOWED_ON_NONLEAF:
        flash(u'部门人员不为空时无法删除', 'danger')
        return redirect(request.referrer)
    flash(u'分组 %s 删除成功' % org_ou, 'success')
    return redirect(url_for('admin.list_orgs'))
