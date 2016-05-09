# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

import itsdangerous
from serbia.core import ldap_manage
from serbia.core import ldap
from serbia.service import MailService
from serbia.utils.auth import login_web
from serbia.utils.auth import logout_web
from serbia.utils.auth import web_auth_required
from . import bp


@bp.route('/account/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('web/login.html')

    # LDAP login
    uid = request.form.get('uid')
    password = request.form.get('password')

    if not ldap.bind_user(uid, password):
        flash(u'用户名和密码不匹配', 'danger')
        return redirect(url_for('web.login'))

    if not ldap._user_in_auth_groups(uid):
        flash(u'你还没有登录的权限，请联系管理员开通', 'danger')
        return redirect(url_for('web.login'))

    # ldap_user = ldap.get_user_details(uid)
    is_admin = ldap._user_in_groups(uid, current_app.config['LDAP_ADMIN_GROUP'])
    user_info = {
        'uid': uid,
        'is_admin': is_admin,
    }
    login_web(user_info)
    return redirect(url_for('web.dashboard'))


@bp.route('/account/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        return render_template('web/forget_password.html')

    email = request.form.get('email')
    user = ldap_manage.client.get_user_by_email(email)

    if not user:
        flash(u'企业邮件并不存在，请重新检查一下~', 'danger')
        return redirect(request.referrer)

    token = itsdangerous.TimestampSigner(current_app.config['RESET_PASSWORD_TOKEN']).sign(user.uid)
    reset_url = url_for('web.reset_password', _external=True) + '?token=%s' % token
    MailService.send_reset_password(email, reset_url)
    flash(u'邮件发送成功', 'success')
    return redirect(request.referrer)


@bp.route('/account/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token')
        try:
            uid = itsdangerous.TimestampSigner(current_app.config['RESET_PASSWORD_TOKEN']).unsign(token)
        except itsdangerous.BadSignature:
            flash(u'链接无效，请检查', 'danger')
        except itsdangerous.SignatureExpired:
            flash(u'链接有效期已过，请重新发送邮件', 'danger')
        return render_template('web/reset_password.html', token=token)

    token = request.form.get('token')
    password = request.form.get('password')

    try:
        uid = itsdangerous.TimestampSigner(current_app.config['RESET_PASSWORD_TOKEN']).unsign(token)
    except itsdangerous.BadSignature:
        flash(u'链接无效，请检查', 'danger')
        return redirect(url_for('web.forget_password'))
    except itsdangerous.SignatureExpired:
        flash(u'链接有效期已过，请重新发送邮件', 'danger')
        return redirect(url_for('web.forget_password'))

    ldap_manage.client.update_user_password(uid, password)
    flash(u'密码更新成功', 'success')
    return redirect(url_for('web.login'))


@bp.route('/account/logout')
@web_auth_required
def logout():
    logout_web()
    return redirect(url_for('web.login'))
