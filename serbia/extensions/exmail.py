# -*- coding: utf-8 -*-

from time import sleep
from functools import wraps

import requests
from werkzeug.contrib.cache import SimpleCache


class Exmail(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._client_id = app.config['EXMAIL_ID']
        self._client_secret = app.config['EXMAIL_SECRET']
        self._cache_client = SimpleCache()
        self.access_token_cache_url = 'exmail:access_token'

    def _gen_access_token(self):
        url = 'https://exmail.qq.com/cgi-bin/token'
        payload = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'client_credentials',
        }
        r = requests.post(url, data=payload)
        r_dict = r.json()
        return (r_dict['access_token'], r_dict['expires_in'])

    @property
    def access_token(self):
        access_token = self._cache_client.get(self.access_token_cache_url)
        if not access_token:
            access_token, expired_secs = self._gen_access_token()
            self._cache_client.set(self.access_token_cache_url, access_token, expired_secs)
        return access_token

    def get_user(self, email):
        url = 'http://openapi.exmail.qq.com:12211/openapi/user/get'
        headers = { 'Authorization': 'Bearer %s' % self.access_token }
        payload = {'alias': email}
        r = requests.post(url=url, data=payload, headers=headers)
        r_dict = r.json()
        return r_dict

    def update_user(self, email, update_dict):
        print update_dict
        url = 'http://openapi.exmail.qq.com:12211/openapi/user/sync'
        update_dict['action'] = 3
        update_dict['alias'] = email
        # update_dict['md5'] = 0
        headers = { 'Authorization': 'Bearer %s' % self.access_token }
        r = requests.post(url=url, data=update_dict, headers=headers)
        print r
        return r

    def update_password(self, email, password):
        return self.update_user(email, {'password': password})

    def add_user(self, email, name, password, org):
        url = 'http://openapi.exmail.qq.com:12211/openapi/user/sync'
        add_dict = {
            'action': 2,
            'alias': email,
            'name': name,
            'password': password,
            'md5': 0,
            'partypath': org,
            'opentype': 1,
        }
        headers = { 'Authorization': 'Bearer %s' % self.access_token }
        r = requests.post(url=url, data=add_dict, headers=headers)
        print r.text
        print r.status_code

    def delete_user(self):
        pass

if __name__ == '__main__':
    exmail = Exmail(EXMAIL_ID, EXMAIL_SECRET)
    print exmail.access_token
    # print exmail.add_user('test@liwushuo.com', '测试', 'Abc12345', '技术-产品')
    # print exmail.get_user('test@liwushuo.com')

    # print exmail.update_user('test@liwushuo.com', {'password': 'gMnoq6PQncsFZn'})
    print exmail.update_user('test@liwushuo.com', {'opentype': 2})
