import os
from flask import Flask, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager

network_health_app = Flask(__name__)
network_health_app.config.from_object(os.environ.get('app_env'))
jwt = JWTManager(network_health_app)
api = Api(network_health_app, prefix='/v1')
blacklist = set()
from neh_apps.uscc_login.uscc_app_login import *
from resources.auth import Authenticate
from resources.refresh import Refresh
from resources.logout import Logout
from neh_apps.network_health.ne_health_sms import NeText
from neh_apps.network_health.nh_dashboard import NetworkHealthDashboard
# from resources.sms import Sms

# Add resources via the add_resource method
api.add_resource(Authenticate, '/login')
api.add_resource(Refresh, '/refresh_token')
api.add_resource(Logout, 'logout')
# api.add_resource(SmsNum, '/sms')

network_health_text = NeText.as_view(name='ne_text')
network_health_dashboard = NetworkHealthDashboard.as_view(name='nh_dashboard')
login_view = Login.as_view(name='uscc_login')
network_health_app.add_url_rule('/sms_register', view_func=network_health_text, methods=['GET', 'POST'])
network_health_app.add_url_rule('/network_health', view_func=network_health_dashboard, methods=['GET'])
network_health_app.add_url_rule('/login', view_func=login_view, methods=['POST', 'GET'])
