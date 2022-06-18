#from .evaluation import Evaluation
from flask      import session
from datetime   import datetime
from app        import mongo
import json

class AdaptativeReasoning:
    @classmethod
    def analyze_question(cls, question, current_user):
        user_info = mongo.db.profiles.aggregate([{'$match': {'username': current_user['username'] }}, {'$project': {'performance': 1, 'answers_time': 1, 'profile': 1, '_id': 0}}])

        ''' a questão não é retornada ao utilizador se:
            - a performance do utilizador não estiver num nível adequado ao domínio que escolheu;
            - o utilizador tiver uma performance muito baixa comparativamente aos utilizadores que receberam a questão;
        '''

        for doc in user_info:
            print("\n\n\n\nInformação do perfil do utilizador:")
            print(doc)
            print("\n\n\n\n")

        print("\n\n\n\nQuestion to send:")
        print(question)
        print("\n\n\n\n")

        return
