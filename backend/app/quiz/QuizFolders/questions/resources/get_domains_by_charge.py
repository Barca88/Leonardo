from flask         import session, render_template, request, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
from datetime      import datetime
from json          import loads
from bson.json_util import dumps
from app           import mongo
import requests
import json
import sys

sys.path.append('../../')

from ... base.enums.user_type import UserType
    
class GetDomainsByCharge(Resource):
    def get(self):
        print('GetDomainsByCharge')
        parser = reqparse.RequestParser()

        parser.add_argument('user_type')
        parser.add_argument('idUser')

        params = parser.parse_args()
        user_role = params.user_type
        id_user = params.idUser

        dictionary = self.dict_domains(user_role, id_user)

        return dumps(dictionary)

    def post(self):
        result = {}
        
        parser = reqparse.RequestParser()

        parser.add_argument('user_type')
        parser.add_argument('idUser')
        parser.add_argument('nomeUser')
        parser.add_argument('editar')

        params = parser.parse_args()
        user_role = params.user_type
        id_user = params.idUser
        name_user = params.nomeUser
        edit = params.editar
            
        dictionary = self.dict_domains(user_role, id_user)
        
        if(edit != None):
            call_edit_domain = self.edit_domain(dictionary, id_user, user_role, name_user)

            dictionary = self.dict_domains(user_role, id_user)

            return dumps({'dictionary': dictionary, 'domain_error': call_edit_domain['domain_error'], 'user_errors': call_edit_domain['user_errors']})
        else:
            if request.content_type == 'text/plain':
                id = request.data.decode("utf-8")

                mongo.db.domains.delete_one({ 'id': id })
        
                dictionary = self.dict_domains(user_role, id_user)

                return dumps({'dictionary': dictionary, 'domain_error': False, 'user_errors': []})
            else:
                call_add_domain = self.add_domain(dictionary, id_user, user_role, name_user)

                dictionary = self.dict_domains(user_role, id_user)

                return dumps({'dictionary': dictionary, 'domain_error': call_add_domain['domain_error'], 'user_errors': call_add_domain['user_errors']})

        return dumps(dictionary)

    def dict_domains(self, role, id_user):
        aux_id_user = int(id_user)
        pipeline = [
            { '$match': { 'users_in_charge.id': str(aux_id_user) } },
            { '$group': {
                '_id': {
                    'study_cycle': '$study_cycle',
                    'scholarity' : '$scholarity'
                },
                'domains': { '$push': '$$ROOT' }
                }
            }
        ]

        if role is 1:
            pipeline.pop(0)

        domains    = mongo.db.domains.aggregate(pipeline)
        
        dictionary = []

        for doc in domains:
            dictionary.append(doc)

        return dictionary

    def insert_domain(self, dictionary, id_user, user_role, name_user, next_id, study_cycle, scholarity, description, users, config):
        user_inserting  = {'id': id_user, 'name': name_user}
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

        if user_role is UserType.ADMIN.value:
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

    def edit_domain(self, dictionay, id_user, user_role, name_user):
        domain_error = False
        user_errors  = []
        edited_domain = request.json

        user_emails  = mongo.db.users.find({}, {'email': 1, '_id': 0})
        emails       = []

        for email in user_emails:
            emails.append(email['email'])

        for user_in_charge_email in edited_domain["users"]:
            if not user_in_charge_email in emails:
                user_errors.append(user_in_charge_email)

        for domain in mongo.db.domains.find():
            if domain['id'] != edited_domain['id'] and domain['study_cycle'] == edited_domain['study_cycle'] and domain['scholarity'] == edited_domain['scholarity'] and domain['description'] == edited_domain['description']:
                domain_error = True

        users_in_charge = []
        if len(user_errors) == 0 and not domain_error:
            if not edited_domain['users'] is []:
                for user in edited_domain['users']:
                    user_resp = mongo.db.users.find_one({ 'email': user })

                    since = ""
                    until = ""    
                    for domain in mongo.db.domains.find():
                        for user_in_c in domain['users_in_charge']:
                            if user_in_c['email'] == user:
                                since = user_in_c['since']
                                until = user_in_c['until']

                    in_charge = {
                        'id'   : user_resp['id'],
                        'name' : user_resp['name'],
                        'email': user,
                        'since': since, #insertion_date,
                        'until': until #''
                    }
                    users_in_charge.append(in_charge)

            mongo.db.domains.update(
                {'id': edited_domain['id']},
                {'$set': {
                    'study_cycle': edited_domain['study_cycle'],
                    'scholarity': edited_domain['scholarity'],
                    'description': edited_domain['description'],
                    'users_in_charge': users_in_charge, #edited_domain['users'],
                    "config.default_user_level": edited_domain['default_user_level'],
                    "config.high_performance_factor": edited_domain['high_performance_factor'],
                    "config.low_performance_factor": edited_domain['low_performance_factor'],
                    "config.high_skill_factor": edited_domain['high_skill_factor'],
                    "config.low_skill_factor": edited_domain['low_skill_factor'],
                    "config.backlog_factor": edited_domain['backlog_factor'],
                    "config.questions_factor": edited_domain['questions_factor'],
                    "config.min_questions_number": edited_domain['min_questions_number']
                }})

        return {'domain_error': domain_error, 'user_errors': user_errors}

    def add_domain(self, dictionary, id_user, user_role, nome_user):
        domain_error = False
        user_errors  = []
        new_domain   = request.json

        user_emails  = mongo.db.users.find({}, {'email': 1, '_id': 0})
        emails       = []

        for email in user_emails:
            emails.append(email['email'])

        for user_in_charge_email in new_domain["users"]:
            if not user_in_charge_email in emails:
                user_errors.append(user_in_charge_email) #user_email)

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
            self.insert_domain(dictionary, id_user, user_role, nome_user, next_id, study_cycle, scholarity, description, users_in_charge, config)

        return {'domain_error': domain_error, 'user_errors': user_errors}