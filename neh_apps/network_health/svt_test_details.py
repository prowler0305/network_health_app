# Flask
from flask import render_template, redirect, request, url_for
from flask.views import MethodView
from common.common import Common

# Misc
import requests
import json
import os
import time


class SvtDetails(MethodView):
    def __init__(self):
        tems_svt_api_base = "http://sa521-iv-result-api-sa3-auto-test.engapps.uscc.com/iv_results_api/tc/"

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        requesting_test_case = request.args.get('test_case')[0:6]
        lcc_site = request.args.get('lcc_location')

        # TODO: insert call to API here later

        with open("C:\\Users\Owner\IdeaProjects\\network_health_app\\neh_apps\\network_health\\svt_test_details.py") as fh:
            svt_details_dict = json.load(fh)

        print(svt_details_dict)
        return render_template('network_health/svt_test_details.html')

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
