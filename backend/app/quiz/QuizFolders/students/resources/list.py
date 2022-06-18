from flask_restful import reqparse, Resource
from flask         import current_app, make_response, render_template
from app           import mongo

class List(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('description')
        parser.add_argument('study_cycle')
        parser.add_argument('scholarity')

        params = parser.parse_args()
        domain = self.__get_domain(params)
        list   = self.__get_students(domain)

        return current_app.make_response(render_template('table.html', domain=domain, students_list=list))


    def __get_domain(self, params):
        return {
            'description': params.description,
            'study_cycle': params.study_cycle,
            'scholarity' : params.scholarity
        }


    def __get_students(self, domain):
        return mongo.db.users.find({"user_type": 4, "domains": {"$elemMatch": domain}})
