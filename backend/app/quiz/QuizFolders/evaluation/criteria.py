from app         import mongo
from collections import Counter

class Criteria:
    def __init__(self, domain, sub_domain):
        self.domain = domain['_id']
        setattr(self,'_id',  {'$ne' :''})
        #self.study_cycle = domain['study_cycle']
        #self.scholarity = domain['scholarity']
        self.subdomain = sub_domain

    def set_difficulty_level(self,  value=None):
        if not value:
            print(self._id)
            #'study_cycle': self.study_cycle, 'scholarity': self.scholarity
            config = mongo.db.domains.find_one({ '_id': self.domain  }, { '_id': 0, 'config': 0 })
            print('config')
            self.difficulty_level = str(int(config['default_user_level']))
            #self.difficulty_level = '1'
        else:
            self.difficulty_level = str(value)

    def set_precedence(self, questions_ids_list=None):
        if not questions_ids_list:
            self.precedence = []
        else:
            
            questions_ids_set = set(questions_ids_list)
            setattr(self, '$or', [
                { 'precedence': { '$size': 0 } },
                { 'precedence': { '$not': { '$elemMatch': { '$nin': list(questions_ids_set) } } } }
            ])
            

    def set_id(self, thrown_questions_ids):
        print('setId   didn\'t have a [0]. its working?')
        repetitions_counter    = Counter(thrown_questions_ids)
        questions_ids_set      = set(thrown_questions_ids)
        excluded_questions_ids = []
        query_filter           = { '_id': { '$in': list(questions_ids_set) } }
        query_projection       = {  'repetitions': 1 }

        questions              = mongo.db.question.find(query_filter, query_projection)

        for question in questions:
            _id          = question['_id']
            repetitions = int(question['repetitions'])

            if repetitions is 0 or repetitions < repetitions_counter[_id]:
                excluded_questions_ids.append(question['_id'])

        self._id = { '$nin': excluded_questions_ids }
