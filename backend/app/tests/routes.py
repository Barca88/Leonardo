from flask import Blueprint, request, make_response
from flasgger import swag_from
from modules.database.models.test import Test
from modules.database.models.test_log import TestLog
from modules.validation.test_schemas import TestSchema
from bson.json_util import dumps
from marshmallow import ValidationError
from datetime import datetime, timedelta
from bson import json_util


from app.tests import blueprint
from flask import render_template, request
from flask_login import login_required
from app import dadosFolio
import os
from app import mongo, token_required

tests_api = Blueprint('tests', __name__)


@blueprint.route('', methods=['GET'])
def get_all_tests():
    print(get_all_tests)
    #type = request.args.get("type")
    #if type == "active":
    #    today = datetime.today().strftime("%Y-%m-%d")
    #    tests = dumps(Test.objects.raw(
    #        {'config.date.start': {'$lte': today}, 'config.date.finish': {'$gte': today}}).project(
    #        {'_id': 0}).values())
#
    #    if len(tests) == 0:
    #        return make_response('There are no active tests stored in the database', 404)
#
    #    return make_response(tests, 200)
#
    #elif type == "nearfuture":
    #    today = datetime.today().strftime("%Y-%m-%d")
    #    tests = dumps(Test.objects.raw(
    #        {'config.date.start': {'$gt': today}}).project({'_id': 0}).values())
#
    #    if len(tests) == 0:
    #        return make_response('There are tests in the near future stored in the database', 404)
#
    #    return make_response(tests, 200)
    #else:
    #    try:
    #        tests = dumps(list(Test.objects.all().project({'_id': 0}).values()))
    #    except Test.DoesNotExist:
    #        return make_response('There are no tests stored in the database', 404)
    tests= [doc for doc in mongo.db.tests.find()]
    print('sending')
    return json_util.dumps({'tests': tests})


@blueprint.route('', methods=['POST'])
def post_test():
    print('post_test')
    data = request.get_json()
    try:
        TestSchema().load(data)
        data['config']['last_updated'] = datetime.today().strftime('%Y-%m-%d')
        t = Test(**data)
        t.save()
        TestLog(action="create", test=t, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()
    except ValidationError as err:
        return make_response(err.messages, 400)
    return make_response('The test was successfully inserted in the database', 201)


@blueprint.route('/<string:test_id>', methods=['DELETE'])
def delete_test(test_id):
    print('delete_test')
    mongo.db.tests.remove({"_id" : test_id})
    return make_response('The test was successfully deleted', 200)


@blueprint.route('/<string:test_id>', methods=['GET'])
def get_test(test_id):
    print('get_test')
    tests = mongo.db.tests.find({"_id": test_id})
    print(tests)
    
    return json_util.dumps({'tests': tests})



@blueprint.route('/results', methods=['POST'])
def get_eval():
    domain = request.form.get('domain')
    subdomains = request.form.get('subdomains').split(',')
    tests = request.form.get('tests').split(',')
    
    if subdomains[0] == '':
        
        subdomains = []
    
    if tests[0] == '':
        print('if')
        tests = []

    if(len(subdomains)==0 and len(tests)==0):
        print(1)
        tests = mongo.db.evaluation.find({"config.domain": domain})
    elif(len(tests)==0 and len(subdomains)>0 ):
        print(2)
        tests = mongo.db.evaluation.find({"config.domain": domain, "config.subdomains" : {"$in": subdomains}})
    elif(len(tests)>0 and len(subdomains)>0 ):
        print(3)
        tests = mongo.db.evaluation.find({"config.domain": domain, "config.subdomains" : {"$in": subdomains}, "testId" : {"$in" : tests}})
    elif(len(tests)>0 and len(subdomains)==0 ):
        print(4)
        tests = mongo.db.evaluation.find({"config.domain": domain, "testId" : {"$in" : tests}})
    print(tests)

    return json_util.dumps({'tests': tests})


@blueprint.route('/<string:test_id>', methods=['PUT'])
def update_test(test_id):
    print('update_test')
    data = request.get_json()
    print(data)
    mongo.db.tests.insert(data)

    return make_response('The test was created', 201)
