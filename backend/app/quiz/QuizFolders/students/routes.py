from flask       import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user
from app         import mongo
from datetime    import datetime, timedelta
from werkzeug.security   import generate_password_hash

blueprint = Blueprint(
    'students_blueprint',
    __name__,
    url_prefix='/students',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def get_user_domains():
    pipeline = [
        { '$match': { 'id': current_user.id } },
        { '$project': { 'domains': 1, '_id': 0 } },
        { '$unwind': '$domains' },
        { '$group': {
            '_id': {
                'study_cycle': '$domains.study_cycle',
                'scholarity' : '$domains.scholarity'
            },
            'domains': { '$push': '$domains' }
        } }
    ]
    user_domains = mongo.db.users.aggregate(pipeline)
    return redirect("http://127.0.0.1:8082/",code=302)


@blueprint.route('/stats', methods=['GET', 'POST'])
@login_required
def get_student_stats():
    student_id            = int(request.args.get('student_id').split('.')[0])
    domain_string         = request.args.get('domain')
    domain                = parse_domain(domain_string)
    student_info          = mongo.db.users.find_one(
        { 'id': student_id },
        { '_id': 0, 'username': 1, 'name': 1, 'email': 1, 'avatar': 1 })

    student_username      = student_info['username']
    student_name          = student_info['name']
    student_email         = student_info['email']
    student_avatar        = student_info['avatar']
    stats                 = mongo.db.profiles.find_one(
        { 'username': student_username, 'profile': { '$elemMatch': { 'domain.description': domain['description'],
                                                                     'domain.study_cycle': domain['study_cycle'],
                                                                     'domain.scholarity' : domain['scholarity'] }}},
        { '_id': 0, 'profile.$': 1 })

    performance_logs      = mongo.db.performance_logs.find(
        { 'username': student_username, 'domain'  : { '$exists': False }},
        { '_id': 0, 'performance': 1, 'timestamp': 1},
        sort = [('timestamp', -1)])

    skill_logs            = mongo.db.skill_logs.find(
        { 'username': student_username, 'domain'  : { '$exists': False }},
        { '_id': 0, 'skill': 1, 'timestamp': 1},
        sort = [('timestamp', -1)])

    question_logs         = get_question_logs(student_username, domain)
    performance           = stats['profile'][0]['hitted'] / stats['profile'][0]['total']
    performance_dif       = weekly_difference(performance, performance_logs, 'performance')
    skill_dif             = weekly_difference(stats['profile'][0]['skill'], skill_logs, 'skill')

    student_stats         = { 'user_level'     : round(stats['profile'][0]['user_level']),
                              'performance'    : round(stats['profile'][0]['hitted'] / stats['profile'][0]['total'] * 100, 2),
                              'skill'          : round(stats['profile'][0]['skill'] * 100, 2),
                              'total_questions': round(stats['profile'][0]['total']),
                              'answers_time'   : round(stats['profile'][0]['answers_time'] / 3600, 2),
                              'performance_dif': round(performance_dif, 2),
                              'skill_dif'      : round(skill_dif, 2) }

    student_personal_info = { 'name'   : student_name,
                              'email'  : student_email,
                              'avatar' : student_avatar}

    students_list         = get_students_list(domain)

    return render_template(
        'student_profile_chart.html',
        stats=student_stats,
        personal_info=student_personal_info,
        students_list=students_list,
        domain=domain,
        question_stats=question_logs)


def get_question_logs(student_username, domain):
    pipeline = [
        { '$match': { 'username': student_username, 'domain.description': domain['description'],
                                                    'domain.study_cycle': domain['study_cycle'],
                                                    'domain.scholarity' : domain['scholarity'] } },
        { '$group': {
            '_id': {
                'subdomain' : '$subdomain',
                'day'       : { '$substr'   : ['$timestamp', 0, 10] }
            },
            'count': { '$sum': 1 }
        } },
        { '$sort': { "_id.day": 1 } }
    ]

    question_logs = mongo.db.question_logs.aggregate(pipeline)
    array_data    = []
    flag          = False

    for log in question_logs:
        data_dict        = {}
        subdomain        = log['_id']['subdomain']
        year, month, day = log['_id']['day'].split('-')
        count            = log['count']
        for i in range(0, len(array_data)):
            if array_data[i]['subdomain'] == subdomain:
                flag = True
                array_data[i]['data'].append([[int(year), int(month), int(day)], count])
                break
        if flag is False:
            data_dict['subdomain'] = subdomain
            data_dict['data']      = [[[int(year), int(month), int(day)], count]]
            array_data.append(data_dict)

    return array_data


def weekly_difference(actual, logs, type):
    week_to_compare = datetime.now() - timedelta(weeks=1)
    log_to_compare  = None
    result          = 0

    for log in logs:
        timestamp = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        if (timestamp + timedelta(days=3)) > week_to_compare and (timestamp - timedelta(days=3)) < week_to_compare:
            log_to_compare = log
            break

    if log_to_compare:
        result = (actual * 100 / log_to_compare[type]) - 100

    return result


def parse_domain(domain):
    description, study_cycle, scholarity = domain.split(',')
    description_value                    = description.split(':')[1].split('\'')[1]
    study_cycle_value                    = study_cycle.split(':')[1].split('\'')[1]
    scholarity_value                     = scholarity.split(':')[1].split('\'')[1]

    domain_request = {'description': description_value,
                      'study_cycle': study_cycle_value,
                      'scholarity' : scholarity_value }

    return domain_request


def get_students_list(domain):
    return mongo.db.users.find({"user_type": 4, "domains": {"$elemMatch": domain}})


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
