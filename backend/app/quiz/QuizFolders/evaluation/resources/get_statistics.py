from flask         import session, render_template, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
import requests
import json
from bson.json_util import dumps, loads
from ..evaluator   import Evaluator
from ..profiler    import Profiler
from app           import mongo

class GetStatistics(Resource):
    def get(self):
        req = {}
        req.update(globals())
        link = str(req.__getitem__('request'))
        user_name = str(link).split('userName=')[1]

        pipeline = [{'$match':{'username': str(user_name)}}]

        list_cursor = list(mongo.db.profiles.find({'username': user_name[0:(str(user_name).__len__() - 8)]}))
        data = dumps(list_cursor[0], indent = 2)

        return data
