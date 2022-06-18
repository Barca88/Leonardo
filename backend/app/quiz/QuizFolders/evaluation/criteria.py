from app         import mongo
from collections import Counter

class Criteria:
    def __init__(self, domain, sub_domain):
        self.domain = domain['_id']
        self._id = domain['_id']
        #self.study_cycle = domain['study_cycle']
        #self.scholarity = domain['scholarity']
        self.subdomain = sub_domain

    def set_difficulty_level(self,  value=None):
        if not value:
            print(self._id)
            #'study_cycle': self.study_cycle, 'scholarity': self.scholarity
            config = mongo.db.domains.find_one({ '_id': self.domain  }, { '_id': 0, 'config': 0 })
            print('config')
            print(config)
            self.difficulty_level = str(int(config['default_user_level']))
            #self.difficulty_level = '1'
        else:
            self.difficulty_level = str(value)

    def set_precedence(self, questions_ids_list=None):
        if not questions_ids_list:
            self.precedence = []
        else:
            questions_ids_set = set(questions_ids_list[0])

            setattr(self, '$or', [
                { 'precedence': { '$size': 0 } },
                { 'precedence': { '$not': { '$elemMatch': { '$nin': list(questions_ids_set) } } } }
            ])

    def set_id(self, thrown_questions_ids):
        print('setId   didn\'t have a [0]. its working?')
        print(thrown_questions_ids)
        repetitions_counter    = Counter(thrown_questions_ids[0])
        questions_ids_set      = set(thrown_questions_ids[0])
        excluded_questions_ids = []
        query_filter           = { 'id': { '$in': list(questions_ids_set) } }
        query_projection       = { '_id': 0, 'id': 1, 'repetitions': 1 }

        questions              = mongo.db.question.find(query_filter, query_projection)

        for question in questions:
            id          = question['id']
            repetitions = int(question['repetitions'])

            if repetitions is 0 or repetitions < repetitions_counter[id]:
                excluded_questions_ids.append(question['id'])

        self.id = { '$nin': excluded_questions_ids }
