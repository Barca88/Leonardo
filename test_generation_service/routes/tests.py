from flask import Blueprint, request, make_response
from flasgger import swag_from
from modules.database.models.test import Test
from modules.database.models.test_log import TestLog
from modules.validation.test_schemas import TestSchema
from bson.json_util import dumps
from marshmallow import ValidationError
from datetime import datetime, timedelta

tests_api = Blueprint('tests', __name__)


@tests_api.route('', methods=['GET'])
@swag_from('../static/docs/tests/get_tests.yml')
def get_all_tests():
    type = request.args.get("type")
    if type == "active":
        today = datetime.today().strftime("%Y-%m-%d")
        tests = dumps(Test.objects.raw(
            {'config.date.start': {'$lte': today}, 'config.date.finish': {'$gte': today}}).project(
            {'_id': 0}).values())

        if len(tests) == 0:
            return make_response('There are no active tests stored in the database', 404)

        return make_response(tests, 200)

    elif type == "nearfuture":
        today = datetime.today().strftime("%Y-%m-%d")
        tests = dumps(Test.objects.raw(
            {'config.date.start': {'$gt': today}}).project({'_id': 0}).values())

        if len(tests) == 0:
            return make_response('There are tests in the near future stored in the database', 404)

        return make_response(tests, 200)
    else:
        try:
            tests = dumps(list(Test.objects.all().project({'_id': 0}).values()))
        except Test.DoesNotExist:
            return make_response('There are no tests stored in the database', 404)
        return make_response(tests, 200)


@tests_api.route('', methods=['POST'])
@swag_from('../static/docs/tests/post_test.yml')
def post_test():
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


@tests_api.route('/<string:test_id>', methods=['DELETE'])
@swag_from('../static/docs/tests/delete_test.yml')
def delete_test(test_id):
    try:
        t = Test.objects.get({"id": test_id})
        TestLog(action="delete", test=t, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()
        t.delete()
    except Test.DoesNotExist:
        return make_response('The test you tried to delete does not exist', 404)
    return make_response('The test was successfully deleted', 200)


@tests_api.route('/<string:test_id>', methods=['GET'])
@swag_from('../static/docs/tests/get_test.yml')
def get_test(test_id):
    try:
        test = dumps(Test.objects.project({'_id': 0}).get(
            {'id': test_id}).to_son().to_dict())
    except Test.DoesNotExist:
        return make_response('The test which id you referenced does not exist', 404)
    return make_response(test, 200)


@tests_api.route('/<string:test_id>', methods=['PUT'])
@swag_from('../static/docs/tests/put_test.yml')
def update_test(test_id):
    data = request.get_json()

    try:
        TestSchema().load(data)
        data['config']['last_updated'] = datetime.today().strftime('%Y-%m-%d')
    except ValidationError as err:
        return make_response(err, 400)

    if data['id'] != test_id:
        return make_response('The provided test Id does not match the request URL', 400)

    try:
        t = Test.objects.get({"id": test_id})
        Test.objects.raw({"id": test_id}).update({"$set": data})
        TestLog(action="update", test=t, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()
        return make_response("The update was successfully applied", 200)
    except Test.DoesNotExist:
        t = Test(**data)
        t.save()
        TestLog(action="create", test=t, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()
        return make_response('The test was created', 201)
