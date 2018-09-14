import os
from flask import jsonify, make_response, current_app, request
from flask_restful import Resource
from common.common import Common


class Sms(Resource):
    """
    """

    def get(self):
        """

        :return:
        """

        imsi_parser = Common.create_api_parser()
        imsi_parser.add_argument('no_alias', choices=['true', 'false'])
        imsi_parser.add_argument('userid', required=True)
        imsi_get_args = Common.parse_request_args(imsi_parser)
        imsi_file_path = Imsi.imsi_subscribers_file + imsi_get_args.get('userid')
        email_file_path = Imsi.email_address_file + imsi_get_args.get('userid')
        return_dict = dict(imsi_list=None, email_list=None)
        no_imsi_yet = {0: "No Imsi(s) being tracked yet."}
        no_email_yet = {0: "No email addresses added yet."}

        if Common.check_path_exists(imsi_file_path):
            list_o_subscriber_ids = []
            dict_of_subscribers = {}

            with open(imsi_file_path, "r") as imsi_fh:
                # current_pos = 0
                for line in imsi_fh:
                    # current_pos = current_pos + len(line)
                    # if '=' not in line:
                    if imsi_get_args.get('no_alias') == 'true':
                        if '(' in line:
                            imsi, alias_right_paren = line.split('(', 1)
                            list_o_subscriber_ids.append(imsi)
                        else:
                            line = line.rstrip('\n')
                            list_o_subscriber_ids.append(line)
                    else:
                        line = line.rstrip('\n')
                        list_o_subscriber_ids.append(line)

            for list_index in range(len(list_o_subscriber_ids)):
                dict_of_subscribers[list_index] = list_o_subscriber_ids[list_index]

            return_dict['imsi_list'] = dict_of_subscribers
        else:
            return_dict['imsi_list'] = no_imsi_yet

        if Common.check_path_exists(email_file_path):
            list_o_emails = []
            dict_of_emails = {}
            with open(email_file_path, "r") as email_fh:
                for line in email_fh:
                    line = line.rstrip('\n')
                    list_o_emails.append(line)

            for list_index in range(len(list_o_emails)):
                dict_of_emails[list_index] = list_o_emails[list_index]

            return_dict['email_list'] = dict_of_emails
        else:
            return_dict['email_list'] = no_email_yet

        if len(return_dict.get('imsi_list')) > 0 and len(return_dict.get('email_list')) > 0:
            response = jsonify(return_dict)

        elif len(return_dict.get('imsi_list')) == 0 and len(return_dict.get('email_list')) > 0:
            return_dict['imsi_list'] = no_imsi_yet
            response = jsonify(return_dict)

        elif len(return_dict.get('email_list')) == 0 and len(return_dict.get('imsi_list')) > 0:
            return_dict['email_list'] = no_email_yet
            response = jsonify(return_dict)

        else:
            return_dict['imsi_list'] = no_imsi_yet
            return_dict['email_list'] = no_email_yet
            response = jsonify(return_dict)

        response.status_code = 200

        return response
