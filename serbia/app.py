# -*- coding: utf-8 -*-

__all__ = ['create_app']

from os import environ

from flask import Flask

from serbia.core import sentry
from serbia.core import ldap
from serbia.core import mail
from serbia.core import ldap_manage
from serbia.core import exmail


def config_from_env(config=None):
    config_map = {
        'dev': 'serbia.settings.development',
        'prod': 'serbia.settings.production',
    }

    flask_env = environ.get('FLASK_ENV', 'dev')
    return config_map.get(flask_env, config_map['dev'])


def create_app(config=None):
    if not config:
        config = config_from_env()

    app = Flask(__name__)

    configure_app(app, config)
    configure_extensions(app)
    configure_filters(app)
    configure_blueprints(app)
    return app


def configure_app(app, config):
    app.config.from_object(config)


def configure_extensions(app):
    mail.init_app(app)

    sentry.init_app(app)

    ldap_manage.init_app(app)

    exmail.init_app(app)

    ldap.init_app(app,
                  users=app.config.get('LDAP_USERS'),
                  groups=app.config.get('LDAP_GROUPS'))



def configure_blueprints(app):
    from serbia.controllers import web_bp, admin_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(admin_bp, url_prefix='/gwserbia')


def configure_filters(app):
    from utils.times import to_iso_datetime, to_iso_date

    app.jinja_env.filters['to_iso_datetime'] = to_iso_datetime
    app.jinja_env.filters['to_iso_date'] = to_iso_date
