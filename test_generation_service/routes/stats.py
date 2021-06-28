from flask import Blueprint, make_response
from modules.database.models.test_result import TestResult
from modules.database.models.domain import Domain
from modules.database.models.test import Test

stats_api = Blueprint('stats', __name__)


@stats_api.route("", methods=['GET'])
def get_stats():
    try:
        domains = Domain.objects.all().values()
    except Domain.DoesNotExist:
        return make_response("There are no domains stored in the database", 404)
    stats = {}
    for d in domains:
        condensed_domain = d['study_cycle'] + "-" + \
            d['scholarity'] + "-" + d['description']
        stats[condensed_domain] = {'tests': {}, 'generalData': {}}

        tests = list(Test.objects.raw(
            {'config.domain.description': d['description'],
             'config.domain.scholarity': d['scholarity'],
             'config.domain.study_cycle': d['study_cycle']}).values())

        if len(tests) == 0:
            return make_response("There are no tests stored in the database",404)

        test_results = list(TestResult.objects.raw(
            {'config.domain.description': d['description'],
             'config.domain.scholarity': d['scholarity'],
             'config.domain.study_cycle': d['study_cycle']}).values())

        if len(test_results) == 0:
            return make_response("There are no test results stored in the database", 404)

        unique_test_results = []
        unique_ids = []
        [(unique_test_results.append(x), unique_ids.append(x['id'])) for x in test_results if x['id'] not in unique_ids]

        assessment_tests = list(
            filter(lambda t: t['config']['test_type'] == 'assessment', tests))
        gauging_tests = list(
            filter(lambda t: t['config']['test_type'] == 'gauging', tests))

        assessment_trs = list(
            filter(lambda tr: tr['config']['test_type'] == 'assessment', unique_test_results))
        gauging_trs = list(
            filter(lambda tr: tr['config']['test_type'] == 'gauging', unique_test_results))

        stats[condensed_domain]['tests']['total'] = {
            'prepared': 0, 'completed': 0, 'questions': 0}
        stats[condensed_domain]['tests']['total']['prepared'] = len(tests)
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
        for tr in test_results:
            total_grades += float(tr['result'])
            best_grade = float(tr['result']) if float(
                tr['result']) > best_grade else best_grade
            worst_grade = float(tr['result']) if float(
                tr['result']) < worst_grade else worst_grade
            for q in tr['questions']:
                right_answers += 1 if float(q['result']) == 1 else 0
                wrong_answers += 1 if float(q['result']) == 0 else 0

        stats[condensed_domain]['generalData']['average'] = total_grades / \
            len(test_results)
        stats[condensed_domain]['generalData']['bestGrade'] = best_grade
        stats[condensed_domain]['generalData']['worstGrade'] = worst_grade
        stats[condensed_domain]['generalData']['rightAnswers'] = right_answers
        stats[condensed_domain]['generalData']['wrongAnswers'] = wrong_answers

    return make_response(stats, 200)
