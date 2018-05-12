# -*- coding: utf-8 -*-

from io import BytesIO
import zipfile

from flask import current_app
from flask import render_template_string
from flask import url_for



class VPNService(object):
    @staticmethod
    def build_vpn_bundle(uid):
        mem_file = BytesIO()
        with zipfile.ZipFile(mem_file, 'w') as zf:
            zf.writestr('vpn_bundle/ca.crt', current_app.config['VPN_CA_CRT'] ,zipfile.ZIP_DEFLATED)
            zf.writestr('vpn_bundle/ta.key', current_app.config['VPN_TA_KEY'] ,zipfile.ZIP_DEFLATED)
            zf.writestr('vpn_bundle/%s.ovpn' % uid, current_app.config['VPN_OVPN_TPL'] ,zipfile.ZIP_DEFLATED)
        mem_file.seek(0)
        return mem_file
