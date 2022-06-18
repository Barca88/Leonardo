from flask         import session, render_template, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
import requests
import json
from ..evaluator   import Evaluator
from ..profiler    import Profiler
from app           import mongo

class GetDomains(Resource):
    def get(self):
        print('-----> GET DOMAINS QUIZ')
        parser = reqparse.RequestParser()

        parser.add_argument('idUser')

        params = parser.parse_args()

        if(1 ==1 ):
            ds = mongo.db.domains.find({}, {'config': 0, 'inserted_at': 0, 'inserted_by': 0, 'subdomains': 0, 'users_in_charge': 0, 'validated_at': 0, 'validated_by': 0})

            domains_in_db = []
            for d in ds:
                domains_in_db.append(d)
            print(domains_in_db)
            return json.dumps(domains_in_db)
        else:
            print('else statment')
            id_user = params.idUser

            pipeline     = [
                { '$match': { 'id': id_user}},
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

            domains = []
            for result in mongo.db.users.aggregate(pipeline):
                domains.append(result)

            return json.dumps(domains)
