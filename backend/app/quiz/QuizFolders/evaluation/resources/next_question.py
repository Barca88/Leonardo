from flask                      import session, render_template, make_response, current_app
from flask_login                import current_user
from flask_restful              import reqparse, Resource
from ..evaluator                import Evaluator
from ..profiler                 import Profiler
from ..rule_based_system        import RuleBasedSystem
from datetime                   import datetime
from ast                        import literal_eval
from app                        import mongo, mongoDW
import json

class NextQuestion(Resource):
    def post(self):
        print('next_Question')
        parser = reqparse.RequestParser()

        parser.add_argument('current_user')
        parser.add_argument('answerObjectDB')
        parser.add_argument('answerObjectDW')
        parser.add_argument('answer')
        parser.add_argument('question')
        parser.add_argument('domain')
        parser.add_argument('subdomain')

        params = parser.parse_args()
        current_user = literal_eval(params.current_user)
        
       
        response_object_db = params.answerObjectDB
        response_object_dw = params.answerObjectDW

        self.save_answer_db_dw(response_object_db, response_object_dw)

        received_question = literal_eval(params.question)

        session['question'] = { 'content': received_question['content'], 'thrown_at': received_question['thrown_at'] }

        #domain = session.get('domain')


        domain = self.__get_domain(literal_eval(params.domain))
        
        result = Evaluator.evaluate_user_answer(params.answer)
        Profiler.update_profile(current_user, result['question'], result['answer'], result['time'])
        user_profile = self.__get_user_profile(domain, current_user)

        question     = Evaluator.throw_question(user_profile, domain, params.subdomain, username=current_user['username'])

        if ( eval( question )['origin'] == 'cbr' ) or ( eval( question )['content'] == {} ):
            content = eval( question )['content']
            number = eval( question )['number']
            thrown_at = eval( question )['thrown_at']

            obj_to_dump = { 'content': content, 'number': number, 'thrown_at': thrown_at }
            print('returning nex_question_if1')
            return json.dumps(obj_to_dump, default=str)
        if( ( eval( question )['content'] != {} ) and ( user_profile != None ) ):
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
            print('returning nex_question_if2')
            return json.dumps(obj_to_dump, default=str)
        else:
            print('returning nex_question_if3')
            return question

        #return current_app.make_response(render_template('question_container.html', question=question))

    def __get_user_profile(self, domain, current_user, edited_user_profile=None):
        if edited_user_profile :
            return {
                'domain'    : Profiler.get_pattern(current_user, domain, edited_user_profile=edited_user_profile),
                'subdomains': Profiler.get_decision_pattern(current_user, domain, edited_user_profile=edited_user_profile)
            }
        else:
            return {
                'domain'    : Profiler.get_pattern(current_user, domain),
                'subdomains': Profiler.get_decision_pattern(current_user, domain)
            }

    def __get_domain(self, domain):
        return {
            '_id': domain['_id']
        }

    def save_answer_db_dw(self, response_object_db, response_object_dw):
        final_response_object_db = eval(response_object_db) 
        
        final_response_object_db['answer']['start_time'] = datetime.strptime(final_response_object_db['answer']['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()
        final_response_object_db['answer']['end_time'] = datetime.strptime(final_response_object_db['answer']['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()

        final_response_object_db['timetag']['date'] = str(final_response_object_db['answer']['end_time']).split('T')[0]
        final_response_object_db['timetag']['time'] = str(final_response_object_db['answer']['end_time']).split('T')[1].split('.')[0]

        mongo.db.answers.insert(final_response_object_db)
        #-----------------------------------------------------------------------------------------------------------------#
        final_response_object_dw = eval(response_object_dw)
        final_response_object_dw['Answer']['Answer_Start_Time'] = datetime.strptime(final_response_object_dw['Answer']['Answer_Start_Time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        final_response_object_dw['Answer']['Answer_End_Time'] = datetime.strptime(final_response_object_dw['Answer']['Answer_End_Time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        final_response_object_dw['Dim_Calendar']['Date'] = datetime.strptime(final_response_object_dw['Dim_Calendar']['Date'].split('T')[0], '%Y-%m-%d') #.isoformat())

        dim_time_in_iso_format = datetime.strptime(final_response_object_dw['Dim_Time'], '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()
        final_response_object_dw['Dim_Time'] = str(dim_time_in_iso_format).split('T')[1].split(':')[0] + ":" + str(dim_time_in_iso_format).split('T')[1].split(':')[1]

        mongoDW.db.dm_answers.insert(final_response_object_dw)

        end_date_update={
            'End_Date': final_response_object_dw['Dim_Calendar']['Date']
        }
        mongoDW.db.materialized.update_one({'Domain':final_response_object_dw['Dim_Question']['Domain']},{'$set':end_date_update},upsert=True)

        return
