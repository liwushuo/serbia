# -*- coding: utf-8 -*-

from flask import jsonify
from flask import current_app


def jsonify_with_data(data={}, code=200):
    """Return a json message(200/201/202)
    """
    return jsonify(data), code


def jsonify_with_list(list, offset, limit, total):
    resp = {'data': list, 'offset': offset, 'limit': limit, 'total': total}
    return jsonify(resp), 200


def jsonify_with_error(err, errors=None, text=None):
    resp = {'message': err[1], 'code': err[0]}
    # for 400 errors
    if errors and current_app.config['ENV'] != 'prod':
        resp['errors'] = errors
    if text:
        resp['text'] = text
    return jsonify(resp), err[0]
