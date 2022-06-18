from .generation import Generation
from app import mongo

class CaseBasedSystem:
    '''
        'Main' of case based reasoning system
    '''
    @classmethod
    def execute_case_based_system(cls, username, domain, subdomain):
        query = mongo.db.profiles.find_one({ "username": username })
        difficulty_level = query['last_question']['difficulty_level']

        gen = Generation(username, difficulty_level, domain, subdomain)
        gen.retrieve()
        gen.reuse()
        gen.revise()
        gen.retain()

        return gen.working_memory['new_question']

        #---------------------------------------------------------------------------------------------------------------#

        #ADICIONAR NA NOVA QUESTÃO, NO CAMPO PRECEDENCE OU REPETITIONS, O ID DE TODAS AS QUESTÕES JÁ RESPONDIDAS PELO ALUNO
        #FAZER ESTA ADIÇÃO SE O CAMPO REPETITIONS OU PRECEDENCE ASSIM O INDICAR - SE A QUESTÃO JÁ FOI LANÇADA TODAS AS VEZES QUE O CAMPO REPETITIONS OU PRECEDENCE O PERMITIR, O ID DA QUESTÃO É INSERIDO NO CAMPO PRECEDENCE OU REPETITIONS DA NOVA QUESTÃO