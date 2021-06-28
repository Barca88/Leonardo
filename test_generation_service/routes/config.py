from flask import Blueprint, make_response
from flasgger import swag_from
from modules.database.models.question import Question
from bson.json_util import dumps

config_api = Blueprint('config', __name__)


@config_api.route('/domains', methods=['GET'])
@swag_from('../static/docs/config/get_domains.yml')
def available_domains():
    questions = Question.objects.raw({})
    cursor = questions.aggregate(
        {'$group': {
            '_id': {
                '$concat': [
                    '$domain.study_cycle',
                    '-',
                    '$domain.scholarity',
                    '-',
                    '$domain.description'
                ]
            },
            'domain': {'$first': '$domain'},
            'subdomains': {'$addToSet': '$subdomain'}
        }}
    )
    result = list(cursor)
    return make_response(dumps(result)), 200
