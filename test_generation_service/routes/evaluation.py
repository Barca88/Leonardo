from flask import Blueprint, request, make_response
from flasgger import swag_from
from marshmallow import ValidationError
from modules.validation.test_schemas import TestEvaluationSchema
from modules.database.models.test import Test
from modules.database.models.test_result import TestResult
from modules.database.models.test_log import TestLog
from random import randint
from datetime import datetime

evaluation_api = Blueprint('resolutions', __name__)


@evaluation_api.route('/<string:test_id>', methods=['GET'])
def request_test(test_id):
    try:
        test = (Test.objects.project({'_id': 0}).get(
            {'id': test_id}).to_son().to_dict())
    except Test.DoesNotExist:
        return make_response('The test which id you referenced does not exist', 404)

    ret = {'id': test_id, 'config': test['config'],
           'compromises': test['compromises'], 'questions': []}
    for q in test['questions']:
        entry = {'id': q['id'], 'header': q['header'],
                 'answering_time': q['answering_time'], 'body': []}
        for o in q['body']:
            entry['body'].append({'answer': o['answer']})
        entry['body'] = sorted(entry['body'], key=lambda _: randint(0, 100))
        ret['questions'].append(entry)

    ret['questions'] = sorted(ret['questions'], key=lambda _: randint(0, 100))

    return ret, 200


@evaluation_api.route('', methods=['POST'])
def evaluate():
    data = request.get_json()
    try:
        TestEvaluationSchema().load(data)
        test = (Test.objects.project({'_id': 0}).get(
            {'id': data['id']}).to_son().to_dict())
    except ValidationError as err:
        return make_response(err.messages, 400)
    except Test.DoesNotExist:
        return make_response('The test which id you referenced does not exist', 404)

    questions = sorted(test['questions'], key=lambda elem: elem['id'])
    user_answers = sorted(data['questions'], key=lambda elem: elem['id'])

    data['questions'] = user_answers
    right_answers = 0
    total_answers = len(data['questions'])

    for ua in user_answers:
        question_id = ua['id']
        for q in questions:
            if q['id'] == question_id:
                selected = sorted(ua['body'], key=lambda elem: elem['answer'])
                ua['body'] = selected
                solution = sorted(q['body'], key=lambda elem: elem['answer'])
                ua['result'] = 0
                for i in range(0, len(selected)):
                    if bool(selected[i]['selected']):
                        r = int(solution[i]['correction']) == 1
                        ua['result'] = 1 if r else 0
                        right_answers += ua['result']
                        selected[i]['correct'] = r
                    else:
                        r = not int(solution[i]['correction']) == 1
                        selected[i]['correct'] = r
    data['result'] = right_answers / total_answers

    tr = TestResult(**data)
    tr.save()
    TestLog(action="solve", test_result=tr, time_stamp=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')).save()

    return data, 200
