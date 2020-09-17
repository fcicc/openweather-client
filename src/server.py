import os
import datetime
import src.database
import src.repository as repository
from flask import Flask, request, jsonify
from src.cities import city_ids
from src.tasks import execute_request
from src.spooler import prepare_spooler_args

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = src.database.get_connection_string()
    src.database.mongo.init_app(app)

    @app.route('/requests/<int:request_id>', methods=['GET'])
    def get_request(request_id): # pylint: disable=unused-variable
        request_info = repository.get_request_process_info(request_id)

        if request_info is None:
            msg = {
                'message': 'Request "{id}" does not exist.'.format(id=request_id)
            }
            return jsonify(msg), 404

        processed_cities_count = request_info['processed_cities_count']
        total_cities_count = request_info['total_cities_count']
        process_percent = float(processed_cities_count) / float(total_cities_count) * 100.0

        return jsonify({'process_percent': process_percent}), 200

    @app.route('/requests', methods=['POST'])
    def post_request(): # pylint: disable=unused-variable
        try:
            data = request.get_json()
            request_id = int(data.get('id'))
        except (AttributeError, ValueError, TypeError):
            msg = {
                'message': 'Missing "id" field. It must exist and have an integer value.'
            }
            return jsonify(msg), 400

        if repository.request_exists(request_id):
            msg = {
                'message': 'Request "{id}" already exists.'.format(id=request_id)
            }
            return jsonify(msg), 400

        repository.insert_request(request_id, datetime.datetime.utcnow(), city_ids)

        cities_per_request = os.environ.get('CITIES_PER_REQUEST')
        task_args = prepare_spooler_args(request_id=request_id, cities_per_request=cities_per_request)
        execute_request(task_args)

        msg = {
            'message': 'Request started successfully.'
        }
        return jsonify(msg), 202, {'Location': '/requests/{id}'.format(id=request_id)}

    return app
