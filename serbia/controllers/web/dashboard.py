# -*- coding: utf-8 -*-



from flask import render_template
from flask import g
from flask import session
from flask import request
from flask import redirect
from flask import flash
from flask import current_app
from flask import send_file

from serbia.service import VPNService
from serbia.core import ldap_manage
from serbia.core import exmail
from serbia.utils.auth import web_auth_required
from serbia.utils.auth import get_web_user_id
from . import bp


@bp.route('/')
@bp.route('/dashboard')
@web_auth_required
def dashboard():
    user = ldap_manage.client.get_user(session['user']['uid'])
    user_groups = ldap_manage.client.list_user_groups(session['user']['uid'])
    return render_template('web/dashboard.html', groups=user_groups, user=user)


@bp.route('/')
@bp.route('/vpn_bundle')
@web_auth_required
def get_vpn_bundle():
    bundle = VPNService.build_vpn_bundle(session['user']['uid'])
    return send_file(bundle, attachment_filename='vpn_%s.zip' % session['user']['uid'], as_attachment=True)


@bp.route('/password', methods=['GET', 'POST'])
@web_auth_required
def update_password():
    if request.method == 'GET':
        user = ldap_manage.client.get_user(session['user']['uid'])
        print user.mail
        return render_template('web/password.html', user=user)

    password = request.form.get('password')
    ldap_manage.client.update_user_password(session['user']['uid'], password)
    flash(u'密码更新成功', 'success')
    return redirect(request.referrer)


@bp.route('/password/exmail', methods=['POST'])
@web_auth_required
def update_exmail_password():
    password = request.form.get('password')
    user = ldap_manage.client.get_user(session['user']['uid'])
    exmail.update_password(user.mail, password)
    flash(u'企业邮箱密码密码更新成功', 'success')
    return redirect(request.referrer)
