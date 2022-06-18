from flask_restful import reqparse, Resource
import json
from app           import mongo

class Rule(Resource):
    def put(self, rule_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rule')
        
        params = parser.parse_args()

        edited_rule = eval(params.rule)

        mongo.db.rules.update(
                {'id': str(rule_id)},
                {'$set': {
                    'domain': edited_rule['domain'],
                    'if_clauses': edited_rule['if_clauses'],
                    'then_clauses': edited_rule['then_clauses']
        }})

        return
    def delete(self, rule_id):
        mongo.db.rules.delete_one({ 'id': str(rule_id) })

        return