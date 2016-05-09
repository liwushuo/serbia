# -*- coding: utf-8 -*-

from functools import wraps

from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import g

WEB_SESSION_KEY = 'user'
WEB_LOGIN_VIEW = 'web.login'


def admin_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if WEB_SESSION_KEY not in session:
            return redirect(url_for(WEB_LOGIN_VIEW))
        if not is_admin():
            return abort(400)
        return f(*args, **kwargs)
    return decorated_function


def is_admin():
    return session[WEB_SESSION_KEY]['is_admin']


def web_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_web_login():
            return redirect(url_for(WEB_LOGIN_VIEW))
        return f(*args, **kwargs)
    return decorated_function


def login_web(user_info):
    session.permanent = True
    session[WEB_SESSION_KEY] = user_info


def logout_web():
    session.pop(WEB_SESSION_KEY, None)


def is_web_login():
    return WEB_SESSION_KEY in session


def get_web_user_id():
    return session.get(WEB_SESSION_KEY, None)
