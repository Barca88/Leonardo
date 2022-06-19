from app           import mongo
from .user_profile import UserProfile

class Profiler:
    @classmethod
    def get_profile(cls, user):
        user = mongo.db.profiles.find_one({ 'username': user['username'] })

        if user is None:
            return None
        else:
            doc                 = {}
            doc['username']     = user['username']
            doc['language']     = user['language']
            doc['type_q']       = None
            doc['domain']       = user['last_domain']
            doc['subdomain']    = user['last_subdomain']
            doc['subsubdomain'] = user['last_subsubdomain']
            doc['student_lvl']  = 1
            doc['performance']  = user['performance']
            doc['skill']        = user['skill']

        return doc


    # Retorna {} (padrão vazio) se nenhum argumento for passado à função
    # Retorna um padrão baseado em domínio e/ou subdomínio e/ou subsubdomínio se os mesmos,
    #    respetivamente, forem passados como argumentos à função
    @classmethod
    def get_pattern(cls, user, domain=None, subdomain=None, subsubdomain=None, edited_user_profile=None):
        user_profile = UserProfile(user['username'])

        pattern      = {}

        if mongo.db.profiles.find_one({ 'username': user['username'] }) is None:
            user_profile.create_profile()

            return pattern
        else:
            print("\nEstou no else do get_pattern\n")


            if (domain is None) and (subdomain is None) and (subsubdomain is None):
                print('if1')
                if edited_user_profile:
                    user_profile.global_pattern_insert(pattern, edited_user_profile)
                else:
                    user_profile.global_pattern_insert(pattern)

            if (not domain is None) and (subdomain is None) and (subsubdomain is None):  
                print('if2')
                query_domain   = {'username': user['username'],
                                  'profile': {'$elemMatch': {'domain': domain['_id'],
                                                             'subdomain': {'$exists': False}}}}

                if edited_user_profile:
                    user_profile.pattern_insert(query_domain, pattern, 'domain', edited_user_profile)
                else:
                    user_profile.pattern_insert(query_domain, pattern, 'domain')

            if (not domain is None) and (not subdomain is None) and (subsubdomain is None):
                print('if3')
                query_subdomain  = {'username': user['username'],
                                    'profile': {'$elemMatch': {'domain': domain['_id'],
                                                               'subdomain': subdomain,
                                                               'subsubdomain': {'$exists': False}}}}

                if edited_user_profile:
                    user_profile.pattern_insert(query_subdomain, pattern, 'subdomain', edited_user_profile)
                else:
                    user_profile.pattern_insert(query_subdomain, pattern, 'subdomain')

            if (not domain is None) and (not subdomain is None) and (not subsubdomain is None):
                print('if4')
                query_subsubdomain = {'username': user['username'],
                                      'profile': {'$elemMatch': {'domain': domain['_id'],
                                                                 'subdomain': 'subdomain',
                                                                 'subsubdomain': 'subsubdomain'}}}

                if edited_user_profile:
                    user_profile.pattern_insert(query_subsubdomain, pattern, 'subsubdomain', edited_user_profile)
                else:
                    user_profile.pattern_insert(query_subsubdomain, pattern, 'subsubdomain')


        return pattern


    # Função para retornar padrão sobre todos os domínios do utilizador
    # Retorna um padrão com os nomes dos domínios e respetivos valores de performance e skill
    # typeCategory = ["domain", "subdomain", "subsubdomain"]
    @classmethod
    def get_decision_pattern(cls, user, domain = None, subdomain = None, edited_user_profile=None):
        user_profile = UserProfile(user['username'])
        pattern      = {}

        if domain == None:
            if edited_user_profile :
                user_profile.query_pattern('domain', pattern, edited_user_profile)
            else:
                user_profile.query_pattern('domain', pattern)
        elif subdomain == None:
            if edited_user_profile:
                user_profile.query_pattern('subdomain', pattern, domain, edited_user_profile)
            else:
                user_profile.query_pattern('subdomain', pattern, domain)
        else:
            if edited_user_profile:
                user_profile.query_pattern('subsubdomain', pattern, domain, subdomain, edited_user_profile)
            else:
                user_profile.query_pattern('subsubdomain', pattern, domain, subdomain)

        return pattern


    @classmethod
    def update_profile(cls, user, question, answer, time):
        user_profile = UserProfile(user['username'])
        framed_time  = user_profile.frame_time(time, question['answering_time'])
        answer       = int(answer)

        query_domain       = {'username': user['username'],
                              'profile': {'$elemMatch': {'domain': { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] },
                                                         'subdomain': {'$exists': False}}}}

        query_subdomain    = {'username': user['username'],
                              'profile': {'$elemMatch': {'domain': { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] },
                                                         'subdomain': question['subdomain'],
                                                         'subsubdomain': {'$exists': False}}}}

        user_profile.check_user_existence('domain', query_domain, question, answer, framed_time, time)
        user_profile.check_user_existence('subdomain', query_subdomain, question, answer, framed_time, time)

        if 'subsubdomain' in question:
            query_subsubdomain = {'username': user['username'],
                                  'profile': {'$elemMatch': {'domain': { 'study_cycle': question['study_cycle'], 'scholarity' : question['scholarity'], 'description': question['domain'] },
                                                             'subdomain': question['subdomain'],
                                                             'subsubdomain': question['subsubdomain']}}}

            user_profile.check_user_existence('subsubdomain', query_subsubdomain, question, answer, framed_time, time)