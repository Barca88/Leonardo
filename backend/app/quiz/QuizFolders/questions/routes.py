from flask                   import Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_login             import login_required, current_user
from json                    import loads
from datetime                import datetime
from math                    import floor, log10
from collections             import OrderedDict
from app                     import mongo
from bson.objectid           import ObjectId
from ..base.enums.user_type  import UserType

blueprint = Blueprint(
    'questions_blueprint',
    __name__,
    url_prefix='/questions',
    template_folder='templates',
    static_folder='static'
)


# =================================================================== QUESTIONS

@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        new_question      = request.json
        new_question_json = loads(new_question)

        if mongo.db.question.find_one() is None:
            new_question_json['number'] = str(1)
        else:
            last_question                    = mongo.db.question.find_one(sort = [('number', -1)])
            new_question_json['number']      = str(int(last_question['number']) + 1)
            new_question_json['inserted_by'] = {
                'id'  : current_user.id,
                'name': current_user.name
            }

        mongo.db.question.insert(new_question_json)

        return list()
    else:
        return render_template('add.html', dict=build_subdomains_dict())

def build_subdomains_dict():
    domains    = mongo.db.domains.find()
    dictionary = {}

    for doc in domains:
        dictionary[doc['description']] = []

        for subdoc in doc['subdomains']:
            dictionary[doc['description']].append(subdoc)

    return dictionary

@blueprint.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    questions      = mongo.db.question.find().sort('domain', 1)
    dictionary     = {}
    current_domain = ''

    for doc in questions:
        print(doc)
        if doc['domain'] != current_domain:
            current_domain                 = doc['domain']
            domain_description             = current_domain #current_domain['description']
            dictionary[domain_description] = []

        dictionary[domain_description].append(doc)

    if request.method == 'POST':
        if request.content_type == 'text/plain':
            to_delete = request.data.decode('utf-8')
            questions = mongo.db.question
            result    = questions.delete_one({ 'number': to_delete })

    return render_template('list.html', dict=dictionary)

# =================================================================== VALIDATION

@blueprint.route('/validation', methods=['GET', 'POST'])
@login_required
def validation():
    questions      = mongo.db.question.find({ 'state' : '0' }).sort('domain', 1)
    dictionary     = {}
    current_domain = ''

    for doc in questions:
        if doc['domain'] != current_domain:
            current_domain             = doc['domain']
            dictionary[current_domain] = []

        dictionary[current_domain].append(doc)

    if request.method == 'POST':
        if request.content_type == 'text/plain':
            to_validate = request.data.decode('utf-8')
            questions   = mongo.db.question
            result      = questions.update_one({ 'number': to_validate }, {'$set': { 'state': '1' }})
        else:
            to_invalidate = loads(request.data)
            # TODO: send message (to_invalidate['message']) to the user that inserted the question
            questions     = mongo.db.question
            result        = questions.delete_one({ 'number': str(to_invalidate['number']) })

    return render_template('validation.html', dict=dictionary)

# =================================================================== DOMAINS

def dict_domains(role):
    pipeline = [
        { '$match': { 'users_in_charge.id': current_user.id } },
        { '$group': {
            '_id': {
                'study_cycle': '$study_cycle',
                'scholarity' : '$scholarity'
            },
            'domains': { '$push': '$$ROOT' }
            }
        }
    ]

    if role == 1:
        pipeline.pop(0)

    domains    = mongo.db.domains.aggregate(pipeline)
    dictionary = []

    for doc in domains:
        dictionary.append(doc)

    return dictionary

@blueprint.route('/domains/add')
@login_required
def domain_args():
    user_role    = current_user.user_type
    dictionary   = dict_domains(user_role)
    domain_error = session.pop('domain_error', None)
    user_errors  = session.pop('user_errors', None)

    return render_template(
        'domains.html',
        dict=dictionary,
        domain_error=domain_error,
        user_errors=user_errors)

def insert_domain(dictionary, next_id, study_cycle, scholarity, description, users, config):
    user_inserting  = { 'id': current_user.id, 'name': current_user.name }
    insertion_date  = datetime.now().isoformat(timespec='seconds')+'Z'
    users_in_charge = []

    if not users is []:
        for user in users:
            user_resp = mongo.db.users.find_one({ 'email': user })
            in_charge = {
                'id'   : user_resp['id'],
                'name' : user_resp['name'],
                'email': user,
                'since': insertion_date,
                'until': ''
            }
            users_in_charge.append(in_charge)

    if current_user.user_type is UserType.ADMIN.value:
        user_validating = user_inserting
        validation_date = insertion_date
    else:
        user_validating = ''
        validation_date = ''

    mongo.db.domains.insert({
        'id'             : next_id,
        'study_cycle'    : study_cycle,
        'scholarity'     : scholarity,
        'description'    : description,
        'subdomains'     : [],
        'inserted_by'    : user_inserting,
        'validated_by'   : user_validating,
        'inserted_at'    : insertion_date,
        'validated_at'   : validation_date,
        'users_in_charge': users_in_charge,
        'config'         : config
	})

    return

def add_domain(dictionary):
    domain_error = False
    user_errors  = []
    new_domain   = loads(request.json)
    user_emails  = mongo.db.users.find({}, {'email': 1, '_id': 0})
    emails       = []

    for email in user_emails:
        emails.append(email['email'])

    for user_in_charge_email in new_domain["users"]:
        if not user_in_charge_email in emails:
            user_errors.append(user_email)

    study_cycle      = new_domain['study_cycle']
    scholarity       = new_domain['scholarity']
    description      = new_domain['description']
    users_in_charge  = new_domain['users']
    high_performance = new_domain['high_performance_factor']
    low_performance  = new_domain['low_performance_factor']
    high_skill       = new_domain['high_skill_factor']
    low_skill        = new_domain['low_skill_factor']
    backlog          = new_domain['backlog_factor']
    questions_factor = new_domain['questions_factor']
    questions_number = new_domain['min_questions_number']
    user_level       = new_domain['default_user_level']
    config           = {
        'high_performance_factor': float(high_performance),
        'low_performance_factor' : float(low_performance),
        'high_skill_factor'      : float(high_skill),
        'low_skill_factor'       : float(low_skill),
        'backlog_factor'         : int(backlog),
        'questions_factor'       : int(questions_factor),
        'default_user_level'     : int(user_level),
        'min_questions_number'   : int(questions_number)
    }

    domains = mongo.db.domains.find_one({}, {'_id': 0, 'id': 1}, sort = [('id', -1)])
    if domains:
        next_id = str(int(domains['id'].split('.')[0]) + 1)
    else:
        next_id = '1'

    for domain in mongo.db.domains.find():
        if domain['study_cycle'] == study_cycle and domain['scholarity'] == scholarity and domain['description'] == description:
            domain_error = True

    if len(user_errors) == 0 and not domain_error:
	    insert_domain(dictionary, next_id, study_cycle, scholarity, description, users_in_charge, config)

    session['domain_error']	= domain_error
    session['user_errors']  = user_errors

    return

@blueprint.route('/domains', methods=['GET', 'POST'])
@login_required
def domains():
    user_role  = current_user.user_type
    dictionary = dict_domains(user_role)
    if request.method == 'POST':
        if request.content_type == 'text/plain':
            id = request.data.decode("utf-8")

            mongo.db.domains.delete_one({ 'id': id })
        else:
            add_domain(dictionary)
        dictionary = dict_domains(user_role)

    return render_template('domains.html', dict=dictionary)

# =================================================================== SUBDOMAINS

@blueprint.route('/subdomains/add')
@login_required
def subdomain_args():
    user_role       = current_user.user_type
    dictionary      = dict_subdomains(user_role)
    subdomain_error = session.pop("subdomain_error", None)
    user_errors     = session.pop("user_errors", None)

    return render_template(
        "subdomains.html",
        dict=dictionary,
        subdomain_error=subdomain_error,
        user_errors=user_errors)


def dict_subdomains(role):
    pipeline = [
        { '$match': { '$or':
            [{ 'users_in_charge.id': current_user.id },
             { 'subdomains.users_in_charge.id': current_user.id }
            ]
        } },
        { '$group': {
            '_id': {
                'study_cycle': '$study_cycle',
                'scholarity' : '$scholarity'
            },
            'domains': { '$push': '$$ROOT' }
            }
        }
    ]

    if role == 1:
        pipeline.pop(0)

    subdomains = mongo.db.domains.aggregate(pipeline)
    dictionary = []

    for group in subdomains:
        dictionary.append(group)

    return dictionary


def insert_subdomain(domain, subdomain, users_in_charge):
    domain_to_update = mongo.db.domains.find_one(
        { 'description': domain['description'], 'study_cycle': domain['study_cycle'], 'scholarity': domain['scholarity'] }
    )
    subdomains_count = len(domain_to_update['subdomains'])

    if not subdomains_count == 0:
        last_subdomain     = domain_to_update['subdomains'][subdomains_count - 1]
        domain_id, last_id = last_subdomain['id'].split('.')
        next_id            = str(int(last_id) + 1)
    else:
        domain_id = domain_to_update['id']
        next_id   = '1'

    subdomain_id = domain_id + '.' + next_id

    inserted_by      = { 'id': current_user.id, 'name': current_user.name }
    inserted_at      = datetime.now().isoformat(timespec='seconds')+'Z'

    if current_user.user_type is UserType.ADMIN.value:
        validated_by = inserted_by
        validated_at = inserted_at
    else:
        validated_by = ''
        validated_at = ''

    new_subdomain = {
        'id'              : subdomain_id,
        'description'     : subdomain,
        'inserted_by'     : inserted_by,
        'validated_by'    : validated_by,
        'inserted_at'     : inserted_at, #Z to keep consistency with JS ISOFormat
        'validated_at'    : validated_at,
        'subsubdomains'   : [],
        'users_in_charge' : users_in_charge
    }
    mongo.db.domains.update(
        { 'description': domain['description'], 'study_cycle': domain['study_cycle'], 'scholarity': domain['scholarity'] },
        { '$push': { 'subdomains': new_subdomain } }
    )

    return

def add_subdomain():
    subdomain_error           = False
    user_errors               = []
    new_subdomain             = loads(request.json)
    insertion_date            = datetime.now().isoformat(timespec='seconds')+'Z'
    new_subdomain_description = new_subdomain['subdomain']
    domain_description        = new_subdomain['domain']['description']
    domain_study_cycle        = new_subdomain['domain']['study_cycle']
    domain_scholarity         = new_subdomain['domain']['scholarity']
    all_subdomains            = mongo.db.domains.find_one(
        { 'description': domain_description, 'study_cycle': domain_study_cycle, 'scholarity' : domain_scholarity },
        { 'subdomains': 1, 'users_in_charge': 1, '_id': 0 }
    )

    if(all_subdomains) is not None:
        for subdomain in all_subdomains['subdomains']:
            if subdomain['description'] == new_subdomain_description:
                subdomain_error = True

        users_in_charge = all_subdomains['users_in_charge']
    
    user_emails     = mongo.db.users.find({}, { 'email': 1, '_id': 0 })
    emails          = []

    for email in user_emails:
        emails.append(email['email'])

    if not new_subdomain['users'] is []:
        for user_in_charge_email in new_subdomain['users']:
            if not user_in_charge_email in emails:
                user_errors.append(user_in_charge_email)
            else:
                user_exists = False
                for user_in_charge in users_in_charge:
                    if user_in_charge['email'] == user_in_charge_email:
                        user_exists = True
                if user_exists is False:
                    user_resp = mongo.db.users.find_one({ 'email': user_in_charge_email })
                    in_charge = {
                        'id'   : user_resp['id'],
                        'name' : user_resp['name'],
                        'email': user_in_charge_email,
                        'since': insertion_date,
                        'until': ''
                    }
                    users_in_charge.append(in_charge)

    if len(user_errors) == 0 and not subdomain_error:
        insert_subdomain(new_subdomain['domain'], new_subdomain_description, users_in_charge)

    session['subdomain_error'] = subdomain_error
    session['user_errors']     = user_errors

    return

@blueprint.route('/subdomains', methods=['GET', 'POST'])
@login_required
def subdomains():
    user_role  = current_user.user_type

    dictionary = dict_subdomains(user_role)

    if request.method == 'POST':
        if request.content_type == 'text/plain':
            subdomain_id      = request.data.decode('utf-8')
            domain_id         = subdomain_id.split('.')[0]

            result = mongo.db.domains.update_one(
                { 'id': domain_id },
                { '$pull': { 'subdomains': { 'id': subdomain_id } } }
            )
            dictionary = dict_subdomains(user_role)
            return render_template('subdomains.html', dict=dictionary)
        else:
            add_subdomain()
        dictionary = dict_subdomains(user_role)

    return render_template('subdomains.html', dict=dictionary)


# =================================================================== SUBSUBDOMAINS

@blueprint.route('/subsubdomains/add')
@login_required
def subsubdomain_args():
    user_role          = current_user.user_type
    dictionary         = dict_subsubdomains(user_role)
    subsubdomain_error = session.pop("subsubdomain_error", None)
    user_errors        = session.pop("user_errors", None)

    return render_template(
        "subsubdomains.html",
        dict=dictionary,
        subsubdomain_error=subsubdomain_error,
        user_errors=user_errors)


def dict_subsubdomains(role):
    pipeline = [
        { '$match': { '$or':
            [{ 'users_in_charge.id': current_user.id },
             { 'subdomains.users_in_charge.id': current_user.id },
             { 'subdomains.subsubdomains.users_in_charge.id': current_user.id }
            ]
        } },
        { '$group': {
            '_id': {
                'study_cycle': '$study_cycle',
                'scholarity' : '$scholarity'
            },
            'domains': { '$push': '$$ROOT' }
            }
        }
    ]

    if role == 1:
        pipeline.pop(0)

    subsubdomains = mongo.db.domains.aggregate(pipeline)
    dictionary    = []

    for group in subsubdomains:
        dictionary.append(group)

    return dictionary


def get_users_in_charge_list(query, new_users, user_errors):
    subdomain_users = mongo.db.domains.find_one( query,
        { '_id': 0, 'subdomains.$.users_in_charge': 1 }
    )
    users_in_charge = subdomain_users['subdomains'][0]['users_in_charge']
    user_emails     = mongo.db.users.find({}, { 'email': 1, '_id': 0 })
    emails          = []
    insertion_date  = datetime.now().isoformat(timespec='seconds')+'Z'

    for email in user_emails:
        emails.append(email['email'])

    if not new_users is []:
        for user_in_charge_email in new_users:
            if not user_in_charge_email in emails:
                user_errors.append(user_in_charge_email)
            else:
                user_exists = False
                for user_in_charge in users_in_charge:
                    if user_in_charge['email'] == user_in_charge_email:
                        user_exists = True
                if user_exists is False:
                    user_resp = mongo.db.users.find_one({ 'email': user_in_charge_email })
                    in_charge = {
                        'id'   : user_resp['id'],
                        'name' : user_resp['name'],
                        'email': user_in_charge_email,
                        'since': insertion_date,
                        'until': ''
                    }
                    users_in_charge.append(in_charge)

    return users_in_charge


def get_new_subsubdomain_id(subsubdomains_list):
    subdomain_id        = subsubdomains_list['subdomains'][0]['id']
    subsubdomains_count = len(subsubdomains_list['subdomains'][0]['subsubdomains'])

    if not subsubdomains_count == 0:
        last_subsubdomain_id = subsubdomains_list['subdomains'][0]['subsubdomains'][subsubdomains_count - 1]['id']
        parsed_id            = last_subsubdomain_id.split('.')[2]
        next_id              = str(int(parsed_id) + 1)
    else:
        next_id = '1'

    new_subsubdomain_id = subdomain_id + '.' + next_id

    return new_subsubdomain_id


def add_subsubdomain():
    subdomain_error                 = False
    user_errors                     = []
    new_subsubdomain_request        = loads(request.json)
    domain                          = new_subsubdomain_request['domain']
    subdomain_description           = new_subsubdomain_request['subdomain']
    subsubdomain_description        = new_subsubdomain_request['subsubdomain']
    query                           = domain
    query['subdomains.description'] = subdomain_description
    subsubdomains_list              = mongo.db.domains.find_one(query, {'_id': 0, 'subdomains.$': 1})

    new_subsubdomain_id = get_new_subsubdomain_id(subsubdomains_list)
    users_in_charge     = get_users_in_charge_list(query, new_subsubdomain_request['users'], user_errors)

    inserted_by         = { 'id': current_user.id, 'name': current_user.name }
    inserted_at         = datetime.now().isoformat(timespec='seconds')+'Z'

    if current_user.user_type is UserType.ADMIN.value:
        validated_by = inserted_by
        validated_at = inserted_at
    else:
        validated_by = ''
        validated_at = ''

    new_subsubdomain         = {
        'id'              : new_subsubdomain_id,
        'description'     : subsubdomain_description,
        'users_in_charge' : users_in_charge,
        'inserted_by'     : inserted_by,
        'validated_by'    : validated_by,
        'inserted_at'     : inserted_at, #Z to keep consistency with JS ISOFormat
        'validated_at'    : validated_at
    }

    for subsubdomain in subsubdomains_list['subdomains'][0]['subsubdomains']:
        if subsubdomain['description'] == subsubdomain_description:
            subdomain_error = True

    if len(user_errors) == 0 and not subdomain_error:
        mongo.db.domains.update(query, { '$push': { 'subdomains.$.subsubdomains': new_subsubdomain } })

    session['subdomain_error'] = subdomain_error
    session['user_errors']     = user_errors

    return


@blueprint.route('/subsubdomains', methods=['GET', 'POST'])
@login_required
def subsubdomains():
    user_role  = current_user.user_type
    dictionary = dict_subsubdomains(user_role)

    if request.method == 'POST':
        if request.content_type == 'text/plain':
            subsubdomain_id                    = request.data.decode('utf-8')
            domain_id, subdomain, subsubdomain = subsubdomain_id.split('.')
            subdomain_id                       = domain_id + '.' + subdomain

            mongo.db.domains.update({'id': domain_id, 'subdomains.id': subdomain_id}, {'$pull': { 'subdomains.$.subsubdomains': {'id': subsubdomain_id} }})
        else:
            add_subsubdomain()

        dictionary = dict_subsubdomains(user_role)

    return render_template('subsubdomains.html', dict=dictionary)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
