from app      import mongo
from datetime import datetime

class UserProfile:
    def __init__(self, username):
        self.username = username

    def create_profile(self):
        doc                                = {}
        doc['username']                    = self.username
        doc['user_level']                  = 2
        doc['total_questions']             = 0
        doc['questions_right']             = 0
        doc['questions_wrong']             = 0
        #doc['questions_answered']         = []
        doc['performance']                 = 0  # Equivalente ao questions_rate no documento do professor
        doc['performance_level']           = 0
        doc['skill']                       = 0
        doc['skill_level']                 = 0
        doc['profile']                     = []
        doc['session_questions_ids']       = []
        doc['sessions_time']               = 0
        doc['questions_time']              = 0
        doc['answers_time']                = 0
        doc['rate_time']                   = 0  # Relação entre o tempo total de resposta e o tempo total de apresentação de questões
        doc['last_session_time']           = 0
        doc['last_domain']                 = None
        doc['last_subdomain']              = None
        doc['last_subsubdomain']           = None
        doc['last_question']               = None
        doc['last_answer']                 = None
        doc['last_difficulty_level']       = None
        doc['last_access']                 = None   # Data e hora do último acesso do utilizador ao sistema
        doc['language']                    = 'pt'
        # doc['status']                    =
        # doc['agent']                     =
        doc['opinion']                     = 0
        doc['notes']                       = None
        # doc['performance_log']           = []
        # doc['skill_log']                 = []
        mongo.db.profiles.insert(doc)


    def global_pattern_insert(self, pattern, edited_user_profile=None):
        if edited_user_profile:
            data = []
            data.append(edited_user_profile)
        else:
            query = {'username': self.username}
            proj  = {'_id': 0, 'user_level': 1, 'performance': 1, 'skill': 1, 'session_questions_ids': 1}
            data  = mongo.db.profiles.find(query, proj)

        for user_profile in data:
            performance           = user_profile['performance']
            skill                 = user_profile['skill']
            user_level            = user_profile['user_level']
            session_questions_ids = user_profile['session_questions_ids']

            pattern['performance']           = performance
            pattern['skill']                 = skill
            pattern['user_level']            = user_level
            pattern['session_questions_ids'] = session_questions_ids


    def pattern_insert(self, query, pattern, query_type, edited_user_profile=None):
        print(query)
        
        if edited_user_profile:
            data = []
            data.append(edited_user_profile)
        else:
            proj = {'_id': 0, 'profile.$': 1, 'session_questions_ids': 1, 'user_level': 1}
            data = mongo.db.profiles.find(query, proj)
        
        for user_profile in data:
            print('userp userp')
            print(user_profile)
            skill                 = user_profile['profile'][0]['skill']
            performance           = user_profile['profile'][0]['hitted'] / user_profile['profile'][0]['total']
            session_questions_ids = user_profile['session_questions_ids']
            user_level            = user_profile['user_level']

            pattern['performance']           = performance
            pattern['skill']                 = skill
            pattern['session_questions_ids'] = session_questions_ids
            pattern['user_level']            = user_level

            if query_type is 'domain':
                wrong_backlog            = user_profile['profile'][0]['wbacklog']
                right_backlog            = user_profile['profile'][0]['rbacklog']
                pattern['right_backlog'] = right_backlog
                pattern['wrong_backlog'] = wrong_backlog
        print('pattern userp')
        print(pattern)

    def query_pattern(self, type_category, pattern, domain = None, subdomain = None, edited_user_profile=None):
        pattern_data = []
        if edited_user_profile:
            if type_category == 'domain':
                for doc in edited_user_profile['profile']:
                    if not 'subdomain' in doc:
                        pattern_data.append(doc)
            elif type_category == 'subdomain':
                for doc in edited_user_profile['profile']:
                    if( ( doc['domain'] == domain ) and ( 'subdomain' in doc ) and ( not 'subsubdomain' in doc ) ):
                        pattern_data.append(doc)
            else:
                for doc in edited_user_profile['profile']:
                    if( ( doc['domain'] == domain ) and ( doc['subdomain'] == subdomain ) and ( 'subsubdomain' in doc ) ):
                        pattern_data.append(doc)
        else:
            pipeline = []

            pipeline.append({'$match': {'username': self.username}})
            pipeline.append({'$unwind': '$profile'})
            pipeline.append({'$project': {'profile': 1, '_id': 0}})

            if type_category == 'domain':
                pipeline.append({'$match': {'profile.subdomain': None}})
            elif type_category == 'subdomain':
                pipeline.append({'$match': {'profile.domain': domain}})
                pipeline.append({'$match': {'profile.subdomain': {'$ne': None}}})
                pipeline.append({'$match': {'profile.subsubdomain': None}})
            else:
                pipeline.append({'$match': {'profile.domain': domain}})
                pipeline.append({'$match': {'profile.subdomain': subdomain}})
                pipeline.append({'$match': {'profile.subsubdomain': {'$ne': None}}})

            pattern_data = mongo.db.profiles.aggregate(pipeline)

        list              = []
        performances_list = []
        skills_list       = []

        for doc in pattern_data:
            list.append(doc['profile'][type_category])
            skills_list.append(doc['profile']['skill'])
            performances_list.append((doc['profile']['hitted'] / doc['profile']['total']))

        pattern['list']         = list
        pattern['performances'] = performances_list
        pattern['skills']       = skills_list


    def frame_time(self, time, max_time):
        framed_time = 1 - ((time * 1) / int(max_time))
        return framed_time


    def check_user_existence(self, query_type, query, question, answer, framed_time, time):
        print('query')
        print(query)
        user = mongo.db.profiles.find_one(query)

        if user is None:
            if query_type == 'domain':
                self.create_field(question, answer, framed_time, time, domain = question['domain']  )
            elif query_type == 'subdomain':
                self.create_field(question, answer, framed_time, time, domain =   question['domain'] , subdomain = question['subdomain'])
            else:
                self.create_field(question, answer, framed_time, time, domain =   question['domain'] ,
                                 subdomain = question['subdomain'], subsubdomain = question['subsubdomain'])
        else:
            self.update_field(answer, framed_time, time, query, query_type, question)


    def create_hypermedia_fields(self, doc, question, answer):
        ''''if not question["images"] == "":
            doc['hypermedia_images_total'] = 1

            if answer is 1:
                doc['hypermedia_images_hitted'] = 1
            else:
                doc['hypermedia_images_hitted'] = 0

        elif not question["videos"] == "":
            doc['hypermedia_audio_visual_total'] = 1

            if answer is 1:
                doc['hypermedia_audio_visual_hitted'] = 1
            else:
                doc['hypermedia_audio_visual_hitted'] = 0'
                '''


    def create_field(self, question, answer, framed_time, time, domain = None, subdomain = None, subsubdomain = None):
        doc = {}

        if not domain is None:
            doc['domain'] = domain

        if not subdomain is None:
            doc['subdomain'] = subdomain

        else:
            doc['user_level']         = 2
            doc['q_in_current_level'] = 1
            doc['answers_time']       = time
            doc_type_field_total      = question['type_'] + "_total"
            doc_type_field_hitted     = question['type_'] + "_hitted"
            doc[doc_type_field_total] = 1

            self.create_hypermedia_fields(doc, question, answer)

            if answer is 1:
                doc['rbacklog']            = 1
                doc['wbacklog']            = 0
                doc[doc_type_field_hitted] = 1
            else:
                doc['rbacklog']            = 0
                doc['wbacklog']            = 1
                doc[doc_type_field_hitted] = 0

        if not subsubdomain is None:
            doc['subsubdomain'] = subsubdomain

        doc['hitted'] = answer
        doc['total']  = 1
        doc['skill']  = framed_time
        query_filter = {'username': self.username}
        query_update = {'$push': {'profile': doc}}

        mongo.db.profiles.update(query_filter, query_update)

        if (not domain is None) and (subdomain is None) and (subsubdomain is None):
            self.create_logs((doc['hitted'] / doc['total']), doc['skill'], question, { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] })
            self.update_general_fields(question, answer, framed_time, time)


    def update_hypermedia_fields(self, user_profile, question_images, question_videos, answer, inc_doc, set_doc):
        if not question_images == "":
            if 'hypermedia_images_total' in user_profile:
                inc_doc['profile.$.hypermedia_images_total']  = 1
                inc_doc['profile.$.hypermedia_images_hitted'] = answer
            else:
                set_doc['profile.$.hypermedia_images_total']  = 1
                set_doc['profile.$.hypermedia_images_hitted'] = answer

        if not question_videos == "":
            if 'hypermedia_audio_visual_total' in user_profile:
                inc_doc['profile.$.hypermedia_audio_visual_total']  = 1
                inc_doc['profile.$.hypermedia_audio_visual_hitted'] = answer
            else:
                set_doc['profile.$.hypermedia_audio_visual_total']  = 1
                set_doc['profile.$.hypermedia_audio_visual_hitted'] = answer


    def update_type_fields(self, user_profile, question_type, answer, inc_doc, set_doc):
        type_field_total  = question_type + '_total'
        type_field_hitted = question_type + '_hitted'
        field_total       = 'profile.$.' + type_field_total
        field_hitted      = 'profile.$.' + type_field_hitted

        if type_field_total in user_profile:
            inc_doc[field_total]  = 1
            inc_doc[field_hitted] = answer

        else:
            set_doc[field_total] = 1
            set_doc[field_hitted] = answer


    def update_field(self, answer, framed_time, time, query, type_category, question):
        query_update = {}
        data         = mongo.db.profiles.find_one(query, {'_id': 0, 'profile.$': 1})
        user_profile = data['profile'][0]

        performance_log = 0
        skill_log       = 0

        old_skill         = user_profile['skill']
        old_total         = user_profile['total']
        new_skill         = ((old_skill * old_total) + framed_time) / (old_total + 1)
        skill_log         = new_skill
        old_right_answers = user_profile['hitted']
        performance_log   = (old_right_answers + answer) / (old_total + 1)
        inc_doc           = {'profile.$.hitted': answer, 'profile.$.total': 1}
        set_doc           = {'profile.$.skill': new_skill}

        if type_category is 'domain':
            self.update_type_fields(user_profile, question['type'], answer, inc_doc, set_doc)
            self.update_hypermedia_fields(user_profile, question['images'], question['videos'], answer, inc_doc, set_doc)
            inc_doc['profile.$.q_in_current_level'] = 1
            inc_doc['profile.$.answers_time']       = time

            if answer is 1:
                inc_doc['profile.$.rbacklog'] = 1
                set_doc['profile.$.wbacklog'] = 0
            else:
                inc_doc['profile.$.wbacklog'] = 1
                set_doc['profile.$.rbacklog'] = 0

        query_update   = {'$inc': inc_doc,
                          '$set': set_doc}

        mongo.db.profiles.update(query, query_update)

        if type_category is 'domain':
            profile = mongo.db.profiles.find(query, {'_id': 0, 'profile.$': 1})

            for p in profile:
                self.update_user_level(question, p, query)

            self.create_logs(performance_log, skill_log, question, { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] })
            self.update_general_fields(question, answer, framed_time, time)


    def update_user_level(self, question, profile, query):
        #config = mongo.db.domains.find_one(question['domain'], {'_id': 0, 'config': 1})
        config = mongo.db.domains.find_one({ 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] }, {'_id': 0, 'config': 1})

        current_user_level      = profile['profile'][0]['user_level']
        questions_in_curr_level = profile['profile'][0]['q_in_current_level']
        performance             = profile['profile'][0]['hitted'] / profile['profile'][0]['total']
        skill                   = profile['profile'][0]['skill']
        rbacklog                = profile['profile'][0]['rbacklog']
        wbacklog                = profile['profile'][0]['wbacklog']

        backlog    = config['config']['backlog_factor'] * current_user_level
        rquestions = round(config['config']['min_questions_number'] + config['config']['questions_factor'] * current_user_level)

        high_performance_level = config['config']['high_performance_factor'] + current_user_level * 0.04
        low_performance_level  = config['config']['low_performance_factor'] + current_user_level * 0.04

        high_skill_level = config['config']['high_skill_factor'] + current_user_level * 0.03
        low_skill_level  = config['config']['low_skill_factor'] + current_user_level * 0.08

        if ((questions_in_curr_level >= rquestions and performance >= high_performance_level and skill >= high_skill_level) or rbacklog >= backlog) and current_user_level < 5:
            inc_doc = {'profile.$.user_level': 1}
            set_doc = {'profile.$.rbacklog': 0, 'profile.$.q_in_current_level': 0}

            query_update = {'$inc': inc_doc,
                            '$set': set_doc}

            mongo.db.profiles.update(query, query_update)

        if ((questions_in_curr_level >= rquestions and performance < low_performance_level and skill <= low_skill_level) or wbacklog >= backlog) and current_user_level > 0:
            inc_doc = {'profile.$.user_level': -1}
            set_doc = {'profile.$.wbacklog': 0, 'profile.$.q_in_current_level': 0}

            query_update = {'$inc': inc_doc,
                            '$set': set_doc}

            mongo.db.profiles.update(query, query_update)


    def update_general_fields(self, question, answer, framed_time, time):
        user = mongo.db.profiles.find_one({'username': self.username})

        global_user_level = self.get_global_user_level()
        performance       = (user['questions_right'] + answer) / (user['total_questions'] + 1)
        skill             = (user['skill'] * user['total_questions'] + framed_time) / (user['total_questions'] + 1)

        if 'subsubdomain' in question:
            last_subsubdomain = question['subsubdomain']
        else:
            last_subsubdomain = None

        push_doc          = {'session_questions_ids': question['_id']}
        set_doc           = {
            'user_level'       : global_user_level,
            'performance'      : performance,
            'skill'            : skill,
            'last_domain'      : { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] },
            'last_subdomain'   : question['subdomain'],
            'last_subsubdomain': last_subsubdomain,
            'last_question'    : question
        }

        inc_doc           = {'total_questions': 1,
                             'answers_time'   : time}

        if answer is 1:
            set_doc['last_answer'] = 'right'
            inc_doc['questions_right'] = 1
        else:
            set_doc['last_answer'] = 'wrong'
            inc_doc['questions_wrong'] = 1

        query_update = {
            '$inc' : inc_doc,
            '$set' : set_doc,
            '$push': push_doc
        }

        mongo.db.profiles.update({'username': self.username}, query_update)

        self.create_logs(performance, skill, question)


    def get_global_user_level(self):
        pipeline = []

        pipeline.append({ '$match': { 'username': self.username } })
        pipeline.append({ '$unwind': '$profile' })
        pipeline.append({ '$project': { 'profile': 1, '_id': 0 } })
        pipeline.append({ '$match': { 'profile.subdomain': None } })

        pattern_data  = mongo.db.profiles.aggregate(pipeline)
        count         = 0
        total_domains = 0

        for data in pattern_data:
            count += data['profile']['user_level']
            total_domains += 1

        global_user_level = round(count / total_domains)

        return global_user_level


    def create_logs(self, performance, skill, question, domain=None):
        date                   = str(datetime.now())
        insert_performance_log = {
            'username'   : self.username,
            'performance': performance,
            'timestamp'  : date
        }
        insert_skill_log       = {
            'username' : self.username,
            'skill'    : skill,
            'timestamp': date
        }
        insert_question_log    = {
            'username' : self.username,
            'header'   : question['header'],
            'domain'   : question['domain'],
            'subdomain': question['subdomain'],
            'timestamp': date,
        }

        if not domain is None:
            insert_performance_log['domain'] = domain
            insert_skill_log['domain']       = domain

        mongo.db.performance_logs.insert(insert_performance_log)
        mongo.db.skill_logs.insert(insert_skill_log)
        mongo.db.question_logs.insert(insert_question_log)