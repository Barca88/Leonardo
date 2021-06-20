from flask import Blueprint, jsonify
from flasgger import swag_from

index_api = Blueprint('index', __name__)


@index_api.route('/', methods=['GET'])
@swag_from('../static/docs/index/index.yml')
def index():
    answer = {
        "message": "Hello World"
    }
    return jsonify(answer), 200
