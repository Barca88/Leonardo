from flask_login   import current_user
from flask_restful import reqparse, Resource
from app           import mongo
from datetime      import datetime

class PostUsers(Resource):
    def post(self):
        print("///////////////////////////////////////////////Estou dentro do método de criar um teste")
        
        parser = reqparse.RequestParser()

        parser.add_argument('novos_users')

        params = parser.parse_args()

        print(params.novos_users)
        
        mongo.db.gam_users.delete_many({})

        print("---------------------------------" + str(len(eval(params.novos_users))))

        for user in eval(params.novos_users):
            mongo.db.gam_users.insert(user)

        return
