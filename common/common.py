import os
from flask import flash, json
from requests import Response
from config import network_health_app_dir
import json


class Common(object):
    """
    Common class that encapsulates static methods for common functionality.

    """

    @staticmethod
    def check_path_exists(path):
        """
        Check if a file exists within the USCC-ENG-API file structure.

        :param path: Path to the directory or file
        :return: True or False the directory or file exists
        """

        return os.path.exists(path)

    @staticmethod
    def find_file_in_project(file_name: str, path=network_health_app_dir, relative_path: bool=True):
        """
        Find a given file in the application directory tree structure and return its relative path to the root app dir.

        :param file_name:
        :param path: Path to start search top down from. Defaults to the applications root directory.
        :param relative_path: True - path to matching file is relative to :param path. False - absolute path to file.
        :return: list containing the relatives path to all occurrences of the matching file_name
        """

        dir_found = []
        for root, dirs, files in os.walk(path):
            if file_name in files:
                if relative_path:
                    dir_found.append(os.path.join(os.path.relpath(root), file_name))
                else:
                    dir_found.append(os.path.join(root, file_name))

        return dir_found

    @staticmethod
    def create_flash_message(message=None, category_request=None):
        """
        Creates a flask flash message object that can be used on the next HTTP request.

        :param message: Can be a string or an HTTP response object in which the response text which should contain the
        standard HTTP error text will be extracted as the message
        :param category_request: category of the message as documented in flask.helpers.flash()
        :return: Flash object that was created.
        """

        if isinstance(message, Response):
            if 'message' in message:
                message_dict = json.loads(message)
            else:
                message_dict = dict(message=None)
                message_dict['message'] = str(message.status_code) + ':' + message.reason
            return flash(message_dict['message'], category=category_request)
        else:
            return flash(message, category=category_request)

    @staticmethod
    def read_json_file(json_file_path):
        """

        :param json_file_path:
        :return:
        """

        # if os.path.exists(json_file_path):
        if Common.check_path_exists(json_file_path):
            with open(json_file_path) as jsfh:
                return True, json.load(jsfh)

        else:
            return False, "Path: '%s' doesn't exist." % json_file_path
