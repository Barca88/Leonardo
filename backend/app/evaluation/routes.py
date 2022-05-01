from flask import Blueprint, request, make_response
from flasgger import swag_from
from modules.database.models.test import Test
from modules.database.models.test_log import TestLog
from modules.validation.test_schemas import TestSchema
from bson.json_util import dumps
from marshmallow import ValidationError
from datetime import datetime, timedelta

from flask import Blueprint, request, make_response
from app.evaluation import blueprint
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




@blueprint.route('', methods=['GET'])
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


@blueprint.route('', methods=['POST'])
def post_test():
    data = request.get_json()
    data["_id"]=data["_id"] + data["student_id"]
    
    print('post_test\n\n')

    questionsIds = []
    for x in data["questions"]:
        questionsIds.append(x["_id"])


    dataresponse = data
    bodyInt = -1
    ansInt = -1
    totalquestions = 0
    correctAns = 0
    for q in data["questions"]:
        totalquestions += 1
        bodyInt=bodyInt+1
        ansInt = -1
        correct = 0
        for ansGiven in q["body"]:
            
            ansInt = ansInt +1
            print(type(ansGiven["correction"]))
            print(type(ansGiven["selected"]))

            if ansGiven["correction"] == "1" and ansGiven["selected"] == True and "result" not in dataresponse["questions"][bodyInt]["body"][ansInt]:
                print('\nyo1\n')
                if correct == 0:
                    correct += 1


            elif ansGiven["correction"] == 1 and ansGiven["selected"] == "True" :
                print('\nyo2\n')
                if correct == 0:
                    correct += 1


            elif ansGiven["eliminative"] == 1 and "result" not in dataresponse["questions"][bodyInt]["body"][ansInt]:
                correct = -1
                print('\nyo3\n')


            elif ansGiven["eliminative"] == 1:
                correct = -1
                print('\nyo4\n')

               
            print(correct)
        if correct == 1:
            correctAns += 1
        dataresponse["questions"][bodyInt]["result"]= correct  

        print(dataresponse)    
        res = "{:.2f}".format((correctAns / totalquestions) * 100)
        dataresponse["result"]= res


            
    mongo.db.evaluation.update({"_id" : data["_id"],  "finished" :  0 }, dataresponse, True)
            
    #print(dataresponse)


    
    return json_util.dumps({'tests': dataresponse})


@blueprint.route('/<string:test_id>', methods=['DELETE'])
def delete_test(test_id):
    try:
        t = Test.objects.get({"id": test_id})
        TestLog(action="delete", test=t, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()
        t.delete()
    except Test.DoesNotExist:
        return make_response('The test you tried to delete does not exist', 404)
    return make_response('The test was successfully deleted', 200)


@blueprint.route('/<string:test_id>', methods=['GET'])
def get_test(test_id):
    print('get1 eval')
    print('get_test')
    tests = mongo.db.tests.find({"_id": test_id})
    print(tests)
    
    return json_util.dumps({'tests': tests})

@blueprint.route('/check/<string:test_id>', methods=['GET'])
def get_check(test_id):
    evaluation = mongo.db.evaluation.find({"_id": test_id})
    return json_util.dumps({'exists': 1, 'questions' : evaluation})
    

@blueprint.route('/<string:test_id>', methods=['PUT'])
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
