from flask_login   import current_user
from flask_restful import reqparse, Resource
from app           import mongo
from datetime      import datetime

class CreateTest(Resource):
    def post(self):
        print("Estou dentro do método de criar um teste")
        parser = reqparse.RequestParser()

        parser.add_argument('study_cycle')
        parser.add_argument('scholarity')
        parser.add_argument('length')
        parser.add_argument('domain')

        params = parser.parse_args()
        domain = mongo.db.domains.find_one({ 'id': params.domain })

        mongo.db.tests.insert({
            'user_id'    : current_user.id,
            'length'     : params.length,
            'questions'  : [],
            'description': 'Teste exemplo',
            'study_cycle': params.study_cycle,
            'scholarity' : params.scholarity,
            'domain'     : {
                'id'         : domain['id'],
                'description': domain['description']
            },
            'created_at' : datetime.now().isoformat(timespec='seconds')+'Z',
            'updated_at' : datetime.now().isoformat(timespec='seconds')+'Z',
        })
