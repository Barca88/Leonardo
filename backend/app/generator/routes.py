from flask import Blueprint, request, make_response
from app.generator import blueprint
from flasgger import swag_from
from marshmallow import ValidationError
from modules.validation.test_schemas import TestConfiguration, TestEditSchema
from modules.database.models.question import Question
from modules.logic.generator import generate_test
from modules.database.models.test import Test



from flask import render_template, request, flash, send_from_directory
from flask_login import login_required
from app import mongo, token_required, admin_required, photo_auth, write_log
from os import path, remove, rename, replace
from werkzeug.security import generate_password_hash
import datetime
from os.path import join, dirname, realpath
from shutil import copyfile, move
###### este é meu
import json 
import csv
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)

generator_api = Blueprint('generator', __name__)


def calculate_drifts(questions, xnr, xdifficulty):
    nr = len(questions)
    difficulty = 0

    for q in questions:
        difficulty += int(q['difficulty_level'])
    difficulty /= nr

    return (nr - xnr), (difficulty - xdifficulty)


def get_query_filter(filter_data):
    questions_filter = {}
    if 'language' in filter_data.keys():
        questions_filter['language'] = filter_data['language']
    if 'question_types' in filter_data.keys():
        questions_filter['type'] = {'$in': filter_data['question_types']}
    if 'domain' in filter_data.keys():
        questions_filter['domain.study_cycle'] = filter_data['domain']['study_cycle']
        questions_filter['domain.scholarity'] = filter_data['domain']['scholarity']
        questions_filter['domain.description'] = filter_data['domain']['description']
    if 'subdomains' in filter_data.keys():
        questions_filter['subdomain'] = {'$in': filter_data['subdomains']}
    if 'subsubdomains' in filter_data.keys():
        questions_filter['subsubdomain'] = {
            '$in': filter_data['subsubdomains']}

    return questions_filter


@blueprint.route('/new', methods=['POST'])
def Generate_test():
    print('inGenerator\n')
    data = request.get_json()
    print(data)
    editing = request.args.get('editing')
    question_pool = list(mongo.db.question.find({"subdomain": { "$in": data['config']['subdomains'] }}))

    for x in question_pool:
        print(x)

    #try:
    #    TestConfiguration().load(data)
    #    if Test.objects.raw({"id": data['_id']}).count() > 0 and editing != 'true':
    #        return make_response("CONFLICT"), 409
    #except ValidationError as err:
    #    return make_response(err.messages, 400)

    #questions_filter = get_query_filter(data['config'])
    #question_pool = Question.objects.raw(
    #    questions_filter).project({'_id': 0, '_cls': 0})
    #question_pool = list(question_pool.aggregate(
    #    {
    #        '$addFields': {
    #            'mandatory_count': {
    #                '$size': {
    #                    '$filter': {
    #                        'input': '$body',
    #                        'as': 'item',
    #                        'cond': {
    #                            '$eq': ['$$item.mandatory', True]
    #                        }
    #                    }
    #                }
    #            }
    #        }
    #    },
    #    {
    #        '$match': {
    #            'mandatory_count': {
    #                '$lte': data['config']['maximum_displayed_answers']
    #            }
#
    #        }
    #    },
    #    {
    #        '$project': {
    #            'mandatory_count': 0
    #        }
    #    }
    #))
    number_questions = data['config']['number_questions']
    if len(question_pool) < number_questions:
        return make_response("NOT_ENOUGH_QUESTIONS"), 422
    total_time = data['config']['total_time'] 
    avg_difficulty = data['config']['avg_difficulty']
    displayed_answers = data['config']['maximum_displayed_answers']
    result = generate_test(question_pool, number_questions, displayed_answers,
                           total_time, avg_difficulty)
    if len(result) == 0:
        return make_response("COULDN'T_SOLVE"), 422

    nr_drift, difficulty_drift = calculate_drifts(
        result, number_questions, avg_difficulty)
    print('returning')
    return {
        '_id': data['config']['_id'],
        'questions': result,
        'config': data['config'],
        'compromises': {
            'number_questions': nr_drift,
            'avg_difficulty': difficulty_drift
        }
    }, 200


@generator_api.route('/edit', methods=['POST'])
@swag_from('../static/docs/generator/edit_test.yml')
def edit_test():
    data = request.get_json()
    try:
        TestEditSchema().load(data)
    except ValidationError as err:
        return make_response(err.messages, 400)

    replace = data['replace']
    questions = data['test']['questions']
    test_config = data['test']['config']
    displayed_answers = test_config['maximum_displayed_answers']
    ids = [q['_id'] for q in questions]

    questions = [q for i, q in enumerate(questions) if i not in replace]

    questions_filter = get_query_filter(data['test']['config'])
    questions_filter['_id'] = {'$nin': ids}
    question_pool = Question.objects.raw(
        questions_filter).project({'_id': 0, '_cls': 0})
    question_pool = list(question_pool.aggregate(
        {
            '$addFields': {
                'mandatory_count': {
                    '$size': {
                        '$filter': {
                            'input': '$body',
                            'as': 'item',
                            'cond': {
                                '$eq': ['$$item.mandatory', True]
                            }
                        }
                    }
                }
            }
        },
        {
            '$match': {
                'mandatory_count': {
                    '$lte': test_config['maximum_displayed_answers']
                }

            }
        },
        {
            '$project': {
                'mandatory_count': 0
            }
        }
    ))

    if len(question_pool) < len(replace):
        return make_response("NOT_ENOUGH_QUESTIONS"), 422

    time_buf = 0
    for q in questions:
        time_buf += int(q['answering_time'])

    nr_to_replace = int(test_config['number_questions']) - len(questions)
    time_to_replace = int(test_config['total_time']) - time_buf
    difficulty_to_replace = int(test_config['avg_difficulty'])

    result = generate_test(question_pool, nr_to_replace,
                           displayed_answers, time_to_replace, difficulty_to_replace)

    if len(result) == 0:
        return make_response("COULDN'T_SOLVE"), 422

    for q in result:
        questions.append(q)

    nr_drift, difficulty_drift = calculate_drifts(questions, int(test_config['number_questions']),
                                                  int(test_config['avg_difficulty']))
    return {
        '_id': data['test']['_id'],
        'questions': questions,
        'config': data['test']['config'],
        'compromises': {
            'number_questions': nr_drift,
            'avg_difficulty': difficulty_drift
        }
    }, 200
