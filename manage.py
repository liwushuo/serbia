#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['app', 'manager']

import os

from flask_script import Manager
from werkzeug.contrib.fixers import ProxyFix

from serbia.app import create_app

flask_env = os.environ.get('FLASK_ENV', 'dev')

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
