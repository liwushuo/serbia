# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from serbia.core import ldap_manage
from serbia.utils.auth import admin_auth_required
from . import bp


@bp.route('/groups')
@admin_auth_required
def list_groups():
    groups = ldap_manage.client.list_groups()
    return render_template('admin/group/list.html', groups=groups)


@bp.route('/groups/add', methods=['GET', 'POST'])
@admin_auth_required
def add_group():
    if request.method == 'GET':
        return render_template('admin/group/add.html')

    cn = request.form.get('cn')
    name = request.form.get('name')
    url = request.form.get('url')
    ldap_manage.client.add_group(cn.encode('utf-8'), name.encode('utf-8'), url.encode('utf-8'))
    flash(u'分组添加成功', 'success')
    return redirect(url_for('admin.list_groups'))


@bp.route('/groups/<group_cn>/update', methods=['GET', 'POST'])
@admin_auth_required
def update_group(group_cn):
    if request.method == 'GET':
        group = ldap_manage.client.get_group(group_cn)
        return render_template('admin/group/update.html', group=group)

    name = request.form.get('name')
    url = request.form.get('url')
    ldap_manage.client.update_group(group_cn.encode('utf-8'), name.encode('utf-8'), url.encode('utf-8'))
    flash(u'分组信息更新成功', 'success')
    return redirect(request.referrer)


@bp.route('/groups/<group_cn>/delete', methods=['POST'])
@admin_auth_required
def delete_group(group_cn):
    ldap_manage.client.delete_group(group_cn)
    flash(u'分组 %s 删除成功' % group_cn, 'success')
    return redirect(url_for('admin.list_groups'))
