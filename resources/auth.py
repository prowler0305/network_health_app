import os
from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from common.common import Common
from neh_api import network_health_app


class Authenticate(Resource):
    @staticmethod
    def post():
        """
        Method to create both access and refresh tokens.

        The create_access_token() creates the JWT access token which has a short lifespan. The create_refresh_token()
        creates a refresh token with a longer life span so that users can refresh their access token when it expires.

        Test using following cURL command after obtain JWT from login method:
            Linux(syntax):
                curl -H "content-type: application/json" -X POST -d '{"username":"test","password":"test"}' http://localhost:5000/v1/login
            Windows(syntax):
                curl -H "Content-Type: application/json" -X POST http://localhost:5000/v1/login -d "{\"username\":\"test\",\"password\":\"test\"}"
        :return:
        """

        automation_groups = dict()
        automation_login_data = dict(art=None, automations=automation_groups, message=None)
        api_cred_path = os.environ.get('api_cred_path')
        if api_cred_path is None:
            network_health_app.logger.critical("Environment Variable 'api_cred_path' is not set.")
            automation_login_data['message'] = "Contact Core Automation Team."
            response = jsonify(automation_login_data)
            response.status_code = 500
            return response

        if not request.is_json:
            response = jsonify({'msg': 'Missing JSON in request'})
            response.status_code = 400
            return response

        params = request.get_json()
        user_name = params.get('username')
        user_password = params.get('password')

        if not user_name:
            response = jsonify({'msg': 'Missing username parameter'})
            response.status_code = 400
            return response
        if not user_password:
            response = jsonify({'msg': 'Missing password parameter'})
            response.status_code = 400
            return response

        if Common.check_path_exists:
            with open(api_cred_path) as afh:
                for line in afh:
                    file_userid, file_password = line.split('=')
                    if file_userid == user_name and file_password.strip('\n') == user_password:
                        automation_login_data['art'] = {'access_token': create_access_token(identity=user_name),
                                                        'refresh_token': create_refresh_token(identity=user_name)
                                                        }
                        response = jsonify(automation_login_data)
                        response.status_code = 200
                        return response

                response = jsonify({'msg': 'Bad username or password'})
                response.status_code = 401
                return response
        else:
            automation_login_data['message'] = "api_cred_path invalid"
            response = jsonify(automation_login_data)
            response.status_code = 500
            return response
