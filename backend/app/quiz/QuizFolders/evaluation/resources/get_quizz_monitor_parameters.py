from flask         import session, render_template, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
import requests
import json
#from ..evaluator   import Evaluator
#from ..profiler    import Profiler
from app           import mongo

class GetQuizzParameters(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username')

        params = parser.parse_args()

        username = params.username

        pipeline = []

        pipeline.append({'$match': {'username': username }})
        pipeline.append({'$project': {'performance': 1, 'answers_time': 1, 'profile': 1, '_id': 0}})

        user_info = mongo.db.profiles.aggregate(pipeline)

        user_info_content = []
        for result in user_info:
            user_info_content.append(result)

        return user_info_content[0]
