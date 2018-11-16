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
        self.tems_svt_api_base = "http://sa521-iv-result-api-sa3-auto-test.engapps.uscc.com/iv_results_api/tc/"
        self.pcap_ftp = 'ftp://ascomftp:ascomftp123@'

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        requesting_test_case = request.args.get('test_case')[0:6]
        lcc_site = request.args.get('lcc')
        lcc_code = None

        lcc_list_resp = requests.get(self.tems_svt_api_base + '/lcc/list')
        if lcc_list_resp.status_code == requests.codes.ok:
            for lcc_location_item in lcc_list_resp.json():
                if lcc_location_item.get('lcc_name').lower() == lcc_site:
                    lcc_code = lcc_location_item.get('lcc_abbrv')
                    lcc_test_details_resp = requests.get(self.tems_svt_api_base + '/tc/' + requesting_test_case + '/' +
                                                         lcc_code)
                    if lcc_test_details_resp.status_code == requests.codes.ok:
                        lcc_details_dict = lcc_test_details_resp.json()
                        lcc_details_result_list = lcc_details_dict.get('results')

                        for details_dict in lcc_details_result_list:
                            if 'UEA_PCAPUploadFile' in details_dict:
                                if details_dict.get('UEA_PCAPUploadFile') is not None:
                                    details_dict['UEA_PCAPUploadFile'] = self.pcap_ftp + \
                                                                         details_dict.get('UEA_PCAPUploadFile')
                                if 'UEB_PCAPUploadFile' in details_dict:
                                    if details_dict.get('UEB_PCAPUploadFile') is not None:
                                        details_dict['UEB_PCAPUploadFile'] = self.pcap_ftp + \
                                                                             details_dict.get('UEB_PCAPUploadFile')
                            for key, value in details_dict.items():
                                if value is None:
                                    details_dict[key] = ""

        return render_template('network_health/svt_test_details.html', svt_list_tc_details=lcc_details_result_list,
                               tc_name=lcc_details_dict.get('tc_name'))
