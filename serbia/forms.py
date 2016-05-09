# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import Email

RE_NICKNAME = '^[A-Za-z0-9_]{5,14}$'


class UserSignupForm(Form):

    username = StringField('username', [InputRequired(), Regexp(regex=RE_NICKNAME)])
    email = StringField('email', [InputRequired(), Email()])
    password = StringField('password', [InputRequired(), Length(min=8, max=20)])
    code = StringField('code', [InputRequired(), Length(min=8, max=20)])



class UserLoginForm(Form):

    email = StringField('email', [InputRequired(), Email()])
    password = StringField('password', [InputRequired(), Length(min=8, max=20)])


class LDAPLoginForm(Form):

    uid = StringField('uid', [InputRequired()])
    password = StringField('password', [InputRequired()])


class UpdatePasswordForm(Form):

    old_password = StringField('password', [InputRequired(), Length(min=8, max=20)])
    new_password = StringField('password', [InputRequired(), Length(min=8, max=20)])


class UpdateSSPasswordForm(Form):

    new_password = StringField('password', [InputRequired(), Length(min=10, max=20)])
