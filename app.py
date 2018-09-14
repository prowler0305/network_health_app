from neh_api import network_health_app


if __name__ == '__main__':

    network_health_app.run(debug=network_health_app.config.get('DEBUG'), threaded=network_health_app.config.get('THREADED'),
                     port=network_health_app.config.get('PORT'), host=network_health_app.config.get('HOST'))
