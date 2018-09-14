from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from neh_api import jwt, blacklist


class Logout(Resource):

    @staticmethod
    @jwt_required
    def delete():
        """

        :return:
        """

        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        response = jsonify({"msg": "Successfully logged out"})
        response.status_code = 200
        return response


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

