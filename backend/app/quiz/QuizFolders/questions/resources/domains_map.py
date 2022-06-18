from flask_restful import reqparse, Resource
from flask         import current_app, make_response, render_template
from app           import mongo

class DomainsMap(Resource):
    def get(self):
        res = mongo.db.domains.find({}, {'_id': 0, 'subdomains': 1, 'description': 1, 'study_cycle': 1, 'scholarity': 1})
        dict = {}

        for r in res:
            dict[r['description']] = r
            
        return dict
