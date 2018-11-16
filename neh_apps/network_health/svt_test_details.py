# Flask
from flask import render_template, redirect, request, url_for
from flask.views import MethodView
from common.common import Common

# Misc
import requests
import json
import os
from dateutil.parser import parse


class SvtDetails(MethodView):
    def __init__(self):
        self.tems_svt_api_base = "http://sa521-iv-result-api-sa3-auto-test.engapps.uscc.com/iv_results_api/tc/"
        self.pcap_ftp = 'ftp://ascomftp:ascomftp123@'
        self.fields_not_to_display_list = ['UEA_PCAPUploadFile', 'UEB_PCAPUploadFile', 'UEA_TestCase',
                                           'UEB_TestCase', 'UEA_MSISDN', 'UEB_MSISDN', 'Sequence']
        self.fields_to_rename_dict = dict(DateTime_Projector='Date/Time', OverallFailureType='Failure Category',
                                          UEA_Duration='UEA Duration(seconds)', UEB_Duration='UEB Duration(seconds)')

    def get(self):
        """

        :return: Renders the html page with all substituted content needed.
        """
        lcc_details_dict = {}
        lcc_details_result_list = []
        requesting_test_case = request.args.get('test_case')[0:6]
        lcc_site = request.args.get('lcc')
        lcc_code = None

        lcc_list_resp = requests.get(self.tems_svt_api_base + '/lcc/list')
        if lcc_list_resp.status_code == requests.codes.ok:
            for lcc_location_item in lcc_list_resp.json():
                if lcc_location_item.get('lcc_name') == 'Roanoake':
                    lcc_location_item['lcc_name'] = 'Roanoke'
                if lcc_location_item.get('lcc_name').lower() == lcc_site:
                    lcc_code = lcc_location_item.get('lcc_abbrv')
                    lcc_test_details_resp = requests.get(self.tems_svt_api_base + '/tc/' + requesting_test_case + '/' +
                                                         lcc_code)
                    if lcc_test_details_resp.status_code == requests.codes.ok:
                        lcc_details_dict = lcc_test_details_resp.json()
                        lcc_details_result_list = lcc_details_dict.get('results')

                        for details_dict in lcc_details_result_list:
                            for field_to_remove in self.fields_not_to_display_list:
                                details_dict.pop(field_to_remove, None)
                            for field_to_rename, new_field_name in self.fields_to_rename_dict.items():
                                details_dict[new_field_name] = details_dict.pop(field_to_rename, None)
                            self.alter_field_data(details_dict)

                                # INFO: Code below is PCAPUploadFile to be displayed in the UI with full FTP URL
                                # if details_dict.get('UEA_PCAPUploadFile') is not None:
                                #     details_dict['UEA_PCAPUploadFile'] = self.pcap_ftp + \
                                #                                          lcc_details_dict.get('pcap_ftp_server') + \
                                #                                          details_dict.get('UEA_PCAPUploadFile')
                                # if 'UEB_PCAPUploadFile' in details_dict:
                                #     if details_dict.get('UEB_PCAPUploadFile') is not None:
                                #         details_dict['UEB_PCAPUploadFile'] = self.pcap_ftp + \
                                #                                              lcc_details_dict.get('pcap_ftp_server') + \
                                #                                              details_dict.get('UEB_PCAPUploadFile')
                            for key, value in details_dict.items():
                                if value is None:
                                    details_dict[key] = ""

        return render_template('network_health/svt_test_details.html', svt_list_tc_details=lcc_details_result_list,
                               tc_name=lcc_details_dict.get('tc_name'))

    def alter_field_data(self, dict_of_test_details):
        """
        For a dictionary of SVT test case details, apply rules to the specific fields needed to alter the data for
        the web display.

        :param dict_of_test_details:
        :return: nothing. Changes dictionary in place.
        """

        if dict_of_test_details.get('Failure Category') is not None:
            if dict_of_test_details.get('Failure Category') == 1:
                dict_of_test_details['Failure Category'] = 'Service'
            else:
                dict_of_test_details['Failure Category'] = 'System'

        if dict_of_test_details.get('UEA_Success') is not None:
            if dict_of_test_details.get('UEA_Success') == 0:
                dict_of_test_details['UEA_Success'] = 'success'
            else:
                dict_of_test_details['UEA_Success'] = 'failed'

        if dict_of_test_details.get('UEB_Success') is not None:
            if dict_of_test_details.get('UEB_Success') == 0:
                dict_of_test_details['UEB_Success'] = 'success'
            else:
                dict_of_test_details['UEB_Success'] = 'failed'

        if dict_of_test_details.get('Date/Time') is not None:
            dict_of_test_details['Date/Time'] = parse(dict_of_test_details.get('Date/Time')).strftime("%m/%d/%Y %H:%M")

        return
