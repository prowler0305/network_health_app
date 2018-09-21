# Flask
from flask import render_template, redirect, request, url_for
from flask.views import MethodView

# USCC
from resources.logout import Logout
from neh_api import api, network_health_app
from neh_apps.network_health.forms import NeTextForm
from common.common import Common

# Misc
import requests
import json
import os
import time


class NetworkHealthDashboard(MethodView):
    def __init__(self):

        # self.imsi_header = {'Authorization': None}
        # self.imsi_tracking_dict = dict(imsi=None,
        #                                userid=None,
        #                                email=None
        #                                )
        # self.imsi_list_get_resp = None
        self.login_redirect_response = None
        self.auto_tracker_url = os.environ.get('auto_tracker_url')
        self.auto_tracker_user = os.environ.get('auto_tracker_user')
        self.auto_tracker_pass = os.environ.get('auto_tracker_pass')
        self.auto_tracker_resp = None
        self.auto_tracker_id = "SA502"

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        # INFO: For now requirement to login is not needed. Open access is fine, if needed uncomment below code to
        # INFO: require authentication via JWT from login app.
        # if request.cookies.get('access_token_cookie') is None:
        #     self.redirect_to_uscc_login()
        #     return self.login_redirect_response

        while True:
            try:
                rc, nh_status_dict = Common.read_json_file(os.environ.get('neh_status'))
                break
            except json.JSONDecodeError:
                time.sleep(3)
                continue

        if rc:
            if os.environ.get('exec_env') != 'local':
                self.auto_tracker_resp = requests.post(url=self.auto_tracker_url,
                                                       data={'automation': self.auto_tracker_id},
                                                       auth=(self.auto_tracker_user, self.auto_tracker_pass),
                                                       verify=False)

            return render_template('network_health/nh_dashboard.html', neh_status=nh_status_dict)

        return render_template('network_health/nh_dashboard.html')

    def redirect_to_uscc_login(self):
        """
        Redirects to the USCC Login application
        :return: redirect response
        """

        self.login_redirect_response = redirect(os.environ.get('login_app') + '?referrer=' +
                                                url_for('ne_text', _external=True))
        return

    @staticmethod
    def data_file_to_dict(file_path):
        """

        :param file_path:
        :return:
        """
        with open(file_path) as fh:
            return json.load(fh)
