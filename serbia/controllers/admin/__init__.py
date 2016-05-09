# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g

bp = Blueprint('admin', __name__)

from . import user
from . import group
from . import org
