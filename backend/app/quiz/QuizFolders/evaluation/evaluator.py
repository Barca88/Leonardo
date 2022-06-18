from .evaluation        import Evaluation
from flask              import session
from datetime           import datetime
from .case_based_system import CaseBasedSystem
from app                import mongo
import json

class Evaluator:
    @classmethod
    def throw_question(cls, user_profile, domain, sub_domain, block_question_generation=None, username=None):
        print('Evaluator')
        print(user_profile)
        print(domain)
        print(sub_domain)
        evaluation = Evaluation(user_profile, domain, sub_domain)
        question = json.loads(evaluation.find_eligible_question())
        print(question)
        origin = ''

        if ( question['choosen_question'] == {} ) and ( not block_question_generation ):
            print(username)
            id_last_answered_question = mongo.db.profiles.find_one( { 'username': username } )['last_question']['_id']
            
            
           
            
            generated_questions = mongo.db.generated_questions.find({}, { "id": 1 })
            generated_questions_ids = []

            for g in generated_questions:
                generated_questions_ids.append(g['id'])
            
            generated_questions_ids.sort()

            if( len( generated_questions_ids ) > 0 ):
                id_last_generated_question = generated_questions_ids[ len( generated_questions_ids ) - 1 ]
            else:
                print('here')
                id_last_generated_question = '-1'

            #print("\nIds:", generated_questions_ids, "\n")
            #print("\nId_last_answered_question:", id_last_answered_question, "\n")
            #print("\nId_last_generated_question:", id_last_generated_question, "\n")

            
            if( id_last_answered_question != id_last_generated_question):
                new_question = CaseBasedSystem.execute_case_based_system(username, domain, sub_domain)
                question_info = { 'choosen_question': new_question, 'list_of_questions': [] }
                question = question_info
                origin = 'cbr'
                

        number     = len(user_profile['domain']['session_questions_ids']) + 1 if user_profile else 1
        thrown_at  = datetime.now()

        session['question'] = { 'content': question['choosen_question'], 'thrown_at': thrown_at }

        #origin = 'db' -> from db
        #origin = 'cbr' -> generated from cbr
        origin = 'cbr' if origin == 'cbr' else 'db'

        quest = { 'content': session['question']['content'], 'choosable_questions': question['list_of_questions'], 'number': number, 'thrown_at': thrown_at, 'origin': origin}

        #return { 'content': question, 'thrown_at': thrown_at }
        return json.dumps(quest, default=str)

    @classmethod
    def evaluate_user_answer(cls, user_answer):
        question          = session['question']

        body              = question['content']['body'] #question['body']

        if(user_answer == "Sem resposta"):
            answer_correction = 0
        else:
            answer_correction = next(option['correction'] for option in body if option['answer'] == user_answer)

        data = question['thrown_at']
        date_time_Object = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')

        answering_time    = (datetime.now() - date_time_Object).total_seconds()
        
        return {
            'question': question['content'],
            'answer'  : answer_correction,
            'time'    : answering_time
        }