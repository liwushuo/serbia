# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from serbia.core import ldap_manage
from serbia.utils.auth import admin_auth_required
from . import bp


@bp.route('/users')
@admin_auth_required
def list_users():
    org = request.args.get('org')
    group = request.args.get('group')
    keyword = request.args.get('keyword')

    orgs = ldap_manage.client.list_orgs()
    groups = ldap_manage.client.list_groups()
    if org:
        users = ldap_manage.client.list_users_by_org(org)
    elif group:
        users = ldap_manage.client.list_users_by_group(group)
    else:
        users = ldap_manage.client.list_users()
    return render_template('admin/user/list.html', users=users, orgs=orgs, groups=groups,
                           org_name=org, group_name=group, keyword=keyword)


@bp.route('/users/add', methods=['GET', 'POST'])
@admin_auth_required
def add_user():
    if request.method == 'GET':
        orgs = ldap_manage.client.list_orgs()
        return render_template('admin/user/add.html', orgs=orgs)

    displayName = request.form.get('displayName')
    sn = request.form.get('sn')
    givenName = request.form.get('givenName')
    uid = request.form.get('uid')
    password = request.form.get('password')
    mail = request.form.get('mail') or ('%s.%s@liwushuo.com' % (givenName, sn))
    cn = '%s %s' % (givenName, sn)
    org = request.form.get('org')

    ldap_manage.client.add_user(displayName.encode('utf-8'), sn.encode('utf-8'), givenName.encode('utf-8'),
                                uid.encode('utf-8'), password.encode('utf-8'), mail.encode('utf-8'),
                                cn.encode('utf-8'), org.encode('utf-8'))
    flash(u'用户 %s 创建成功' % displayName, 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/users/<uid>/update', methods=['GET', 'POST'])
@admin_auth_required
def update_user(uid):
    if request.method == 'GET':
        orgs = ldap_manage.client.list_orgs()
        user = ldap_manage.client.get_user(uid)
        user_groups = ldap_manage.client.list_user_groups(uid)
        user_group_ids = [user_group.cn for user_group in user_groups]
        groups = ldap_manage.client.list_groups()
        for group in groups:
            if group.cn in user_group_ids:
                group.in_group = True
        return render_template('admin/user/update.html', orgs=orgs, uid=uid, user=user, groups=groups)


@bp.route('/users/<uid>/archive', methods=['POST'])
@admin_auth_required
def archive_user(uid):
    ldap_manage.client.archive_user(uid.encode('utf-8'))
    flash(u'用户 %s 离职成功' % uid, 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/users/<uid>/delete', methods=['POST'])
@admin_auth_required
def delete_user(uid):
    ldap_manage.client.delete_user(uid.encode('utf-8'))
    flash(u'用户 %s 删除成功' % uid, 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/users/<uid>/group', methods=['POST'])
@admin_auth_required
def update_user_group(uid):
    new_groups = request.form.getlist('value')
    user_groups = ldap_manage.client.list_user_groups(uid)
    old_groups = [user_group.cn for user_group in user_groups]

    add_ids = list(set(new_groups).difference(set(old_groups)))
    delete_ids = list(set(old_groups).difference(set(new_groups)))

    add_ids = [add_id.encode('utf-8') for add_id in add_ids]
    delete_ids = [delete_id.encode('utf-8') for delete_id in delete_ids]
    ldap_manage.client.add_user_to_groups(uid.encode('utf-8'), add_ids)
    ldap_manage.client.remove_user_from_groups(uid.encode('utf-8'), delete_ids)

    flash(u'用户 %s 组更新成功' % uid, 'success')
    return redirect(request.referrer)


@bp.route('/users/<uid>/org', methods=['POST'])
@admin_auth_required
def update_user_org(uid):
    org = request.form.get('org')
    ldap_manage.client.update_user_org(uid.encode('utf-8'), org.encode('utf-8'))
    flash(u'用户 %s 部门更新成功' % uid, 'success')
    return redirect(request.referrer)


@bp.route('/users/<uid>/password', methods=['POST'])
@admin_auth_required
def update_user_password(uid):
    password = request.form.get('password')
    ldap_manage.client.update_user_password(uid.encode('utf-8'), password)
    flash(u'用户 %s 密码更新成功' % uid, 'success')
    return redirect(request.referrer)
