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


class NeText(MethodView):
    def __init__(self):

        # self.imsi_header = {'Authorization': None}
        # self.imsi_tracking_dict = dict(imsi=None,
        #                                userid=None,
        #                                email=None
        #                                )
        # self.imsi_list_get_resp = None
        self.login_redirect_response = None
        self.neh_text_dir_found_list = Common.find_file_in_project(os.environ.get('neh_sms_file'))

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        # INFO: For now requirement to login is not needed. Open access is fine, if needed uncomment below code to
        # INFO: require authentication via JWT from login app.
        # if request.cookies.get('access_token_cookie') is None:
        #     self.redirect_to_uscc_login()
        #     return self.login_redirect_response

        form = NeTextForm()
        if len(self.neh_text_dir_found_list) != 0:
            neh_file_path = self.neh_text_dir_found_list[0]
            if request.args.get('search_first') is not None and request.args.get('search_first') != '' and \
                    request.args.get('search_last') is not None and request.args.get('search_last') != '':
                search_key = '{} {}'.format(request.args.get('search_first'), request.args.get('search_last'))
                neh_text_dict = self.data_file_to_dict(neh_file_path)

                if neh_text_dict.get(search_key) is not None:
                    # Get the phone number (which is a key in the sub dictionary for the search name)
                    user_phone = list(neh_text_dict.get(search_key).keys())[0]
                else:
                    Common.create_flash_message(message="No phone number for {} has been registered".format(search_key))
            else:
                user_phone = None

        return render_template('network_health/ne_text_tracking.html', form=form, display_phone=user_phone)

    def post(self):
        """
        """

        # INFO: No requirement for being authenticated to add phone number for text message services. If needed
        # INFO: uncomment both 'if' blocks below.
        # if 'logout_btn' in request.form:
        #     self.delete()
        #     return self.login_redirect_response
        #
        # if request.cookies.get('access_token_cookie') is None:
        #     self.redirect_to_uscc_login()
        #     return self.login_redirect_response

        # else:
        #     # INFO: needed if JWT_TOKEN_LOCATION is set to headers as opposed to in cookies
        #     # self.imsi_header['Authorization'] = 'JWT {}'.format(request.cookies.get('access_token_cookie'))
        #     # INFO: With JWT in cookies set the CSRF token is still expected to be in the header for POST to succeed
        #     self.imsi_header['X-CSRF-TOKEN'] = request.cookies.get('csrf_access_token')
        #     self.imsi_header['content_type'] = 'application/json'

        form = NeTextForm()

        if form.validate_on_submit():
            if len(self.neh_text_dir_found_list) != 0:
                neh_text_path = self.neh_text_dir_found_list[0]
                nehtext_file_dict = self.data_file_to_dict(neh_text_path)
                name_key = '{} {}'.format(form.first_name.data, form.last_name.data)

                if name_key not in nehtext_file_dict:
                    nehtext_file_dict[name_key] = {form.phone_num.data: form.carrier.data}

                    with open(neh_text_path, mode='w') as nehwfh:
                        json.dump(nehtext_file_dict, nehwfh)

                Common.create_flash_message(message="Phone Number added")
            else:
                Common.create_flash_message(message="'{}' file not found. Please contact Core Automation Team.".format(os.environ.get('neh_text_file')))

        else:
            if len(form.errors) != 0:
                for form_field, error_message_text in form.errors.items():
                    Common.create_flash_message(message=form_field + ':' + error_message_text[0])

        return render_template('network_health/ne_text_tracking.html', form=form)

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
