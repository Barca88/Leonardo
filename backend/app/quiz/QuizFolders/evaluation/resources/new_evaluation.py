from typing                 import Tuple
from flask                  import session
from flask_login            import current_user
from flask_restful          import reqparse, Resource
import json
from app                    import mongo
from ..evaluator            import Evaluator
from ..profiler             import Profiler
from ..rule_based_system    import RuleBasedSystem
from flask                  import current_app, make_response, render_template, request
from bson.objectid          import ObjectId
from datetime               import datetime

class NewEvaluation(Resource):
    def get(self):
        print('----> new_evaluation')
        parser = reqparse.RequestParser()
        parser.add_argument('_id')
        parser.add_argument('domain')
        parser.add_argument('study_cycle')
        parser.add_argument('scholarity')
        parser.add_argument('description')
        parser.add_argument('subdomain')
        parser.add_argument('id')
        parser.add_argument('username')
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('gender')
        parser.add_argument('degree')
        parser.add_argument('user_type')
        parser.add_argument('user_level')

        params            = parser.parse_args()

        
        user = {
            'id'         : params.id,
            'username'   : params.username,
            'name'       : params.name,
            'email'      : params.email,
            'gender'     : params.gender,
            'degree'     : params.degree,
            'user_type'  : params.user_type,
            'user_level'  : params.user_level,
        }

        current_user = user
        
        domain            = self.__get_domain(params)
        print('userLEVEEEl')
        print(current_user)
        user_profile      = self.__get_user_profile(domain, current_user)

        session['domain'] = domain

        question          = Evaluator.throw_question(user_profile, domain, params.subdomain, username=current_user['username'])

        if ( eval( question )['origin'] == 'cbr' ) or ( eval( question )['content'] == {} ):
            content = eval( question )['content']
            number = eval( question )['number']
            thrown_at = eval( question )['thrown_at']

            obj_to_dump = { 'content': content, 'number': number, 'thrown_at': thrown_at }

            return json.dumps(obj_to_dump, default=str)
        if( ( eval( question )['content'] != {} ) and ( user_profile != None ) and 1 ==2 ):
            question_to_send = RuleBasedSystem.execute_rule_based_system(current_user, domain, params.subdomain, question)
            
            thrown_at = ''
            number = eval( question )['number']

            obj_to_dump = {}

            if( (len(question_to_send) == 1) and ('status' in question_to_send) ):
                thrown_at = eval( question )['thrown_at']
                obj_to_dump = { 'content': eval( question )['content'], 'number': number, 'thrown_at': thrown_at }
            else:
                thrown_at = datetime.now()
                session['question'] = { 'content': question_to_send, 'thrown_at': thrown_at }

                obj_to_dump = { 'content': question_to_send, 'number': number, 'thrown_at': thrown_at }

            return json.dumps(obj_to_dump, default=str)
        else:
            return question

    def __get_domain(self, params):
        
        return {
            '_id': params._id
            #'scholarity' : params.scholarity,
            #'description': params.description
        }

    def __get_user_profile(self, domain, current_user, edited_user_profile=None):
        print('__get_user_profile')
        print(current_user)
        if edited_user_profile:
            print('edited_user_profile')
            domain_profile = Profiler.get_pattern(current_user, domain, edited_user_profile=edited_user_profile)
        else:
            print('NOT edited_user_profile')
            domain_profile = Profiler.get_pattern(current_user, domain)
        
        print('before domain_profile')
        print('__get_user_profile')
        print(current_user)

        if domain_profile:
            print('domain_profile')
            if edited_user_profile:
                print('domain_profile - edited')
                subdomains_profile = Profiler.get_decision_pattern(current_user, domain, edited_user_profile=edited_user_profile)
            else:
                subdomains_profile = Profiler.get_decision_pattern(current_user, domain)

            return { 'domain': domain_profile, 'subdomains': subdomains_profile }
