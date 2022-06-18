from flask         import session, render_template, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
import requests
import json
from app           import mongo

class GetUsers(Resource):
    def get(self):
        list_cursor = list(mongo.db.gam_users.find({}, {"_id": 0}))

        return json.dumps(list_cursor)
