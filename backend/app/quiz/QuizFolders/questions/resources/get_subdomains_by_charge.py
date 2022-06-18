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

from ...base.enums.user_type import UserType
    
class GetSubdomainsByCharge(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_type')
        parser.add_argument('idUser')

        params = parser.parse_args()
        user_role = params.user_type
        id_user = params.idUser

        dictionary = self.dict_subdomains(int(user_role), id_user)

        return dumps(dictionary)

    def post(self):
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

        dictionary = self.dict_subdomains(int(user_role), id_user)

        if(edit != None):
            call_edit_subdomain = self.edit_subdomain(dictionary, id_user, user_role, name_user)

            dictionary = self.dict_subdomains(int(user_role), id_user)

            return dumps({'dictionary': dictionary, 'subdomain_error': call_edit_subdomain['subdomain_error'], 'user_errors': call_edit_subdomain['user_errors']})
        else:
            if request.content_type == 'text/plain':
                sub_domain_id      = request.data.decode('utf-8')
                domain_id         = sub_domain_id.split('.')[0]

                result = mongo.db.domains.update_one(
                    { 'id': domain_id },
                    { '$pull': { 'subdomains': { 'id': sub_domain_id } } }
                )
                dictionary = self.dict_subdomains(int(user_role), id_user)

                return dumps(dictionary)
            else:
                call_add_subdomain = self.add_subdomain(id_user, user_role, name_user)

                dictionary = self.dict_subdomains(int(user_role), id_user)

                return dumps({'dictionary': dictionary, 'subdomain_error': call_add_subdomain['subdomain_error'], 'user_errors': call_add_subdomain['user_errors']})

        return dumps(dictionary)

    def dict_subdomains(self, role, id_user):
        aux_id_user = int(id_user)

        pipeline = [
            { '$match': { '$or':
                [{ 'users_in_charge.id': str(aux_id_user) },
                { 'subdomains.users_in_charge.id': str(aux_id_user) }
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

        if role is 1:
            pipeline.pop(0)

        sub_domains = mongo.db.domains.aggregate(pipeline)
        dictionary = []

        for group in sub_domains:
            dictionary.append(group)

        return dictionary

    def insert_subdomain(self, domain, subdomain, users_in_charge, id_user, user_role, name_user):
        domain_to_update = mongo.db.domains.find_one(
            { 'description': domain['description'], 'study_cycle': domain['study_cycle'], 'scholarity': domain['scholarity'] }
        )
        sub_domains_count = len(domain_to_update['subdomains'])

        if not sub_domains_count == 0:
            last_subdomain     = domain_to_update['subdomains'][sub_domains_count - 1]
            domain_id, last_id = last_subdomain['id'].split('.')
            next_id            = str(int(last_id) + 1)
        else:
            domain_id = domain_to_update['id']
            next_id   = '1'

        sub_domain_id = domain_id + '.' + next_id

        inserted_by      =  { 'id': id_user, 'name': name_user }
        inserted_at      = datetime.now().isoformat(timespec='seconds')+'Z'

        if user_role is UserType.ADMIN.value:
            validated_by = inserted_by
            validated_at = inserted_at
        else:
            validated_by = ''
            validated_at = ''

        new_subdomain = {
            'id'              : sub_domain_id,
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

    def edit_subdomain(self, dictionay, id_user, user_role, name_user):
        sub_domain_error           = False
        user_errors               = []
        new_subdomain             = request.json

        insertion_date            = datetime.now().isoformat(timespec='seconds')+'Z'
        new_subdomain_description = new_subdomain['subdomain']
        
        domain_description = ""
        domain_study_cycle = ""
        domain_scholarity = ""
        keepCurrent = 0

        if(new_subdomain['domain']['description'] != '' and new_subdomain['domain']['study_cycle'] != '' and new_subdomain['domain']['scholarity'] and
            new_subdomain['domain']['description'] != new_subdomain['currentDomain']['description'] and new_subdomain['domain']['study_cycle'] != new_subdomain['currentDomain']['study_cycle'] and new_subdomain['domain']['scholarity'] != new_subdomain['currentDomain']['scholarity']):
            domain_description        = new_subdomain['domain']['description']
            domain_study_cycle        = new_subdomain['domain']['study_cycle']
            domain_scholarity         = new_subdomain['domain']['scholarity']

            keepCurrent = 0
        else:
            domain_description        = new_subdomain['currentDomain']['description']
            domain_study_cycle        = new_subdomain['currentDomain']['study_cycle']
            domain_scholarity         = new_subdomain['currentDomain']['scholarity']

            keepCurrent = 1
                
        all_subdomains            = mongo.db.domains.find_one(
            { 'description': domain_description, 'study_cycle': domain_study_cycle, 'scholarity' : domain_scholarity },
            { 'subdomains': 1, 'users_in_charge': 1, '_id': 0 }
        )

        users_in_charge = []
        if(all_subdomains) is not None:
            for subdomain in all_subdomains['subdomains']:
                if(subdomain['description'] == new_subdomain_description) and (subdomain['id'] != new_subdomain['idSubdomain']):
                    sub_domain_error = True

            users_in_charge = all_subdomains['users_in_charge']
        
        user_emails     = mongo.db.users.find({}, { 'email': 1, '_id': 0 })
        emails          = []

        for email in user_emails:
            emails.append(email['email'])

        userss_in_charge = []
        if not new_subdomain['users'] is []:
            for user_in_charge_email in new_subdomain['users']:
                if not user_in_charge_email in emails:
                    user_errors.append(user_in_charge_email)
                else:
                    user_exists = False
                    for user_in_charge in users_in_charge:
                        if user_in_charge['email'] == user_in_charge_email:
                            user_exists = True

                            userss_in_charge.append(user_in_charge)
                    if user_exists is False:
                        user_resp = mongo.db.users.find_one({ 'email': user_in_charge_email })
                        in_charge = {
                            'id'   : user_resp['id'],
                            'name' : user_resp['name'],
                            'email': user_in_charge_email,
                            'since': insertion_date,
                            'until': ''
                        }
                        userss_in_charge.append(in_charge)

        if len(user_errors) == 0 and not sub_domain_error:
            if(keepCurrent == 1):
                mongo.db.domains.update({
                    "description": str(domain_description), "study_cycle": str(domain_study_cycle), "scholarity": str(domain_scholarity),
                    "subdomains.id": str(new_subdomain['idSubdomain'])}, {'$set': { "subdomains.$.description": str(new_subdomain['subdomain']), "subdomains.$.users_in_charge": userss_in_charge}
                })
            elif(keepCurrent == 0):
                mongo.db.domains.update_one(
                        { 'description': new_subdomain['currentDomain']['description'], 'study_cycle': new_subdomain['currentDomain']['study_cycle'], 'scholarity' : new_subdomain['currentDomain']['scholarity'] },
                        { '$pull': { 'subdomains': { 'id': str(new_subdomain['idSubdomain']) } } }
                )

                self.insert_subdomain(new_subdomain['domain'], new_subdomain_description, userss_in_charge, id_user, user_role, name_user)

        return {'subdomain_error': sub_domain_error, 'user_errors': user_errors}

    def add_subdomain(self, id_user, user_role, name_user):
        sub_domain_error           = False
        user_errors               = []
        new_subdomain             = request.json

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
                    sub_domain_error = True

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

        if len(user_errors) == 0 and not sub_domain_error:
            self.insert_subdomain(new_subdomain['domain'], new_subdomain_description, users_in_charge, id_user, user_role, name_user)

        return {'subdomain_error': sub_domain_error, 'user_errors': user_errors}