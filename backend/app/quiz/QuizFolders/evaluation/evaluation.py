from app       import mongo
from random    import choice
from .criteria import Criteria
from bson import json_util

class Evaluation:
    def __init__(self, user_profile, domain, sub_domain):
        print('------> Evaluation')
        self.criteria = Criteria(domain, sub_domain)
        self.config   = mongo.db.domains.find_one(domain, { '_id': 0, 'config': 0 })#['config']
        

        if not user_profile:
            self.criteria.set_difficulty_level()
        else:
            print(user_profile)
            self.user_profile = user_profile['domain']

            self.set_criteria_with_user_profile()

    def find_eligible_question(self):
        print('filtro inical')
        print(self.criteria.__dict__)
        filtro = {
            'domain':self.criteria.domain,
            'subdomain' :self.criteria.subdomain,
            'difficulty_level':self.criteria.difficulty_level
        }
        print(self.criteria.__dict__)
        filtered_questions = mongo.db.question.find(self.criteria.__dict__)
        print(filtered_questions.count())
        while not filtered_questions.count():
            #performance = self.user_profile['performance'] if self.user_profile else 0
            performance =  0
            factor      = float(self.config['high_performance_factor'])
            user_level  = int(self.criteria.difficulty_level)

            if performance > factor and user_level < 5:
                self.criteria.set_difficulty_level(value=user_level+1)
            elif user_level > 0:
                self.criteria.set_difficulty_level(value=user_level-1)


            print('filtro while')
            print(filtro)
            filtered_questions = mongo.db.question.find(self.criteria.__dict__)
            print(filtered_questions.count())
            if( ( ( user_level - 1 ) == 0 ) and ( filtered_questions.count() == 0 ) ):
                break

        choosen_question = {}
        
        quests = []
        for q in filtered_questions:
            quests.append(q)

        if( len(quests) > 0):#filtered_questions.count() > 0 ):
            choosen_question = choice(quests) #choice(list(filtered_questions))
        print('obj to return')
        #obj_to_return = { 'choosen_question': choosen_question, 'list_of_questions': quests }

        return json_util.dumps({'choosen_question': choosen_question, 'list_of_questions': quests})

    def set_criteria_with_user_profile(self):
        print(self.user_profile)
        user_level            = self.user_profile['user_level']
        session_questions_ids = self.user_profile['session_questions_ids']
        
        if session_questions_ids:
            print('if')
            self.set_difficulty_level_with_backlog(user_level)
            #proximas duas linhas invertidas
            self.criteria.set_precedence(questions_ids_list=session_questions_ids)
            self.criteria.set_id(session_questions_ids)
        else:
            
            self.criteria.set_difficulty_level(value=user_level)
            self.criteria.set_precedence()

    def set_subdomain(self):
        # APPLY WHEN USERLEVEL IS HIGH
        subdomains_list         = user_profile['subdomains']
        subdomains_performances = user_profile['subdomains_performances']
        lowest_performance      = min(subdomains_performances)
        performance_index       = subdomains_performances.index(lowest_performance)

        return subdomains_list[performance_index]

    def set_difficulty_level_with_backlog(self, user_level):
        domain_backlog     = int(self.config['backlog_factor']) + 2 * user_level
        
        if ('right_backlog' in self.user_profile) and ('wrong_backlog' in self.user_profile):
            user_right_backlog = self.user_profile['right_backlog']
            user_wrong_backlog = self.user_profile['wrong_backlog']

            if (abs(domain_backlog - user_right_backlog) is 1 and user_level < 5) or (abs(domain_backlog - user_wrong_backlog) is 1 and user_level > 0):
                user_level = user_level + 1 if user_right_backlog else user_level - 1

        self.criteria.set_difficulty_level(value=user_level)
