from flask import Blueprint, make_response
from modules.database.models.test_result import TestResult
from modules.database.models.domain import Domain
from modules.database.models.test import Test

from flask import Blueprint, request, make_response
from flasgger import swag_from
from modules.database.models.test import Test
from modules.database.models.test_log import TestLog
from modules.validation.test_schemas import TestSchema
from bson.json_util import dumps
from marshmallow import ValidationError
from datetime import datetime, timedelta
from bson import json_util


from app.stats import blueprint
from flask import render_template, request
from flask_login import login_required
from app import dadosFolio
import os
from app import mongo, token_required

stats_api = Blueprint('stats', __name__)


@blueprint.route("", methods=['GET'])
def get_stats():
    print('get stats')
    try:
        domains = mongo.db.domains.find()
    except Domain.DoesNotExist:
        return make_response("There are no domains stored in the database", 404)
    stats = {}
    for d in domains:
        print(d['_id'])
        condensed_domain = d['_id']
        stats[condensed_domain] = {'tests': {}, 'generalData': {}}

        tests = mongo.db.tests.find({"config.domain" : condensed_domain})

        if len(list(tests.clone())) == 0:
            print('if len(tests) == 0:')
            return make_response("There are no tests stored in the database",404)

        test_results = mongo.db.evaluation.find({"config.domain" : condensed_domain})

        if len(list(test_results.clone())) == 0:
            print('if len(test_results) == 0:')
            return make_response("There are no test results stored in the database", 404)

        unique_test_results = []
        unique_ids = []
        [(unique_test_results.append(x), unique_ids.append(x['_id'])) for x in test_results.clone() if x['_id'] not in unique_ids]

        assessment_tests = list(
            filter(lambda t: t['config']['test_type'] == 'assessment', tests.clone()))
        gauging_tests = list(
            filter(lambda t: t['config']['test_type'] == 'gauging', tests.clone()))

        assessment_trs = list(
            filter(lambda tr: tr['config']['test_type'] == 'assessment', unique_test_results))
        gauging_trs = list(
            filter(lambda tr: tr['config']['test_type'] == 'gauging', unique_test_results))

        stats[condensed_domain]['tests']['total'] = {
            'prepared': 0, 'completed': 0, 'questions': 0}
        stats[condensed_domain]['tests']['total']['prepared'] = len(list(tests.clone()))
        stats[condensed_domain]['tests']['total']['completed'] = len(
            unique_test_results)

        stats[condensed_domain]['tests']['assessment'] = {
            'prepared': 0, 'completed': 0, 'questions': 0}
        stats[condensed_domain]['tests']['assessment']['prepared'] = len(
            assessment_tests)
        stats[condensed_domain]['tests']['assessment']['completed'] = len(
            assessment_trs)

        stats[condensed_domain]['tests']['gauging'] = {
            'prepared': 0, 'completed': 0, 'questions': 0}
        stats[condensed_domain]['tests']['gauging']['prepared'] = len(
            gauging_tests)
        stats[condensed_domain]['tests']['gauging']['completed'] = len(
            gauging_trs)

        for t in assessment_tests:
            questions = len(t['questions'])
            stats[condensed_domain]['tests']['total']['questions'] += questions
            stats[condensed_domain]['tests']['assessment']['questions'] += questions

        for t in gauging_tests:
            questions = len(t['questions'])
            stats[condensed_domain]['tests']['total']['questions'] += questions
            stats[condensed_domain]['tests']['gauging']['questions'] += questions

        total_grades = 0
        best_grade = -1
        worst_grade = 999999
        right_answers = 0
        wrong_answers = 0
        for tr in test_results.clone():
            total_grades += float(tr['result'])
            best_grade = float(tr['result']) if float(
                tr['result']) > best_grade else best_grade
            worst_grade = float(tr['result']) if float(
                tr['result']) < worst_grade else worst_grade
            for q in tr['questions']:
                right_answers += 1 if float(q['result']) == 1 else 0
                wrong_answers += 1 if float(q['result']) == 0 else 0
    
        stats[condensed_domain]['generalData']['average'] = total_grades / \
            len(list(test_results.clone()))
        stats[condensed_domain]['generalData']['bestGrade'] = best_grade
        stats[condensed_domain]['generalData']['worstGrade'] = worst_grade
        print(worst_grade)
        stats[condensed_domain]['generalData']['rightAnswers'] = right_answers
        stats[condensed_domain]['generalData']['wrongAnswers'] = wrong_answers
    print('Done')
    return make_response(stats, 200)
