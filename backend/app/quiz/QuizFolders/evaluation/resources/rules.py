from flask_restful import reqparse, Resource
import json
from app           import mongo

class Rules(Resource):
    def get(self):
        q1 = mongo.db.rules.aggregate( [ { "$group": { "_id": { "domain": "$domain", "study_cycle": "$study_cycle", "scholarity": "$scholarity" }, "rules": { "$push":  { "id": "$id", "if_clauses": "$if_clauses", "then_clauses": "$then_clauses"} } } } ] )

        rules_by_domain = []
        for q in q1:
            rules_by_domain.append(q)

        return json.dumps(rules_by_domain)    

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('rule')
        
        params = parser.parse_args()

        new_rule = eval(params.rule)

        mongo.db.rules.insert(new_rule)

        return