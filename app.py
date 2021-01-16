import os
import requests
import yaml
from http import HTTPStatus
from flask import Flask, request, jsonify, make_response, abort
from waitress import serve

app = Flask(__name__)

CONFIG_YAML_FILE = 'config.yml'
CONFIG_ROUTER = 'routerConfig'
CONFIG_OPTIMIZATION_SERVER = 'optimizationServer'
CONFIG_VROOM = 'vroom'
CONFIG_HOST = 'host'
CONFIG_PORT = 'port'

DEFAULT_ROUTER_PORT = '5000'

DEFAULT_VROOM_HOST = '0.0.0.0'
DEFAULT_VROOM_PORT = '3000'

configuration = \
    {
        CONFIG_ROUTER: {
            CONFIG_PORT: DEFAULT_ROUTER_PORT
        },
        CONFIG_OPTIMIZATION_SERVER: {
            CONFIG_VROOM: {
                CONFIG_HOST: DEFAULT_VROOM_HOST,
                CONFIG_PORT: DEFAULT_VROOM_PORT
            }
        }
    }


@app.route('/', methods=['POST'])
def optimize():
    request_json = request.get_json()
    if request_json == {} or request.content_type != 'application/json':
        abort(HTTPStatus.BAD_REQUEST)

    response_json = {}
    try:
        response = requests.post(url=get_vroom_url(configuration), json=request_json)
        response_json = response.json()
        if response.status_code != HTTPStatus.OK:
            return make_response(response_json, response.status_code)
    except IOError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description='Is vroom properly configured and available?')

    return convert_vroom_output(request_json, response_json)


def get_vroom_url(config):
    vroom_config = config[CONFIG_OPTIMIZATION_SERVER][CONFIG_VROOM]
    return 'http://' + vroom_config[CONFIG_HOST] + ':' + vroom_config[CONFIG_PORT]


def convert_vroom_output(request_json, response_json):
    empty_routes = create_routes_for_unassigned_vehicles(request_json['vehicles'], response_json['routes'])
    return jsonify({
        'totalDeliveryDuration': response_json['summary']['cost'],
        'routes': {**simplify_routes(response_json['routes']), **empty_routes}
    })


def create_routes_for_unassigned_vehicles(vehicles, routes):
    unassigned_vehicles = []
    if len(vehicles) != len(routes):
        all_vehicles = {v['id'] for v in vehicles}
        assigned_vehicles = {r['vehicle'] for r in routes}
        unassigned_vehicles = all_vehicles - assigned_vehicles

    jobs = {i: [] for i in unassigned_vehicles}
    return jobs


def simplify_routes(routes):
    return {route['vehicle']: simplify_steps(route['steps']) for route in routes}


def simplify_steps(steps):
    return [str(step['id']) for step in steps if step['type'] == 'job']


def load_config():
    global configuration
    if os.path.exists(CONFIG_YAML_FILE):
        with open(CONFIG_YAML_FILE, 'r') as ymlfile:
            configuration = {**configuration, **yaml.load(ymlfile, Loader=yaml.BaseLoader)}


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(error):
    return make_response(jsonify({'error': error.name, 'description': error.description}), HTTPStatus.BAD_REQUEST)


@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    return make_response(jsonify({'error': error.name, 'description': error.description}), HTTPStatus.NOT_FOUND)


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    return make_response(jsonify({'error': error.name, 'description': error.description}),
                         HTTPStatus.METHOD_NOT_ALLOWED)


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    return make_response(jsonify({'error': error.name, 'description': error.description}),
                         HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    load_config()
    serve(app, port=configuration[CONFIG_ROUTER][CONFIG_PORT])
