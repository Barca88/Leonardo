from flask         import session, render_template, make_response, current_app
from flask_login   import current_user
from flask_restful import reqparse, Resource
from flask         import request
import requests
import json
#from ..evaluator   import Evaluator
#from ..profiler    import Profiler
from app           import mongo

class GetButtonInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('buttonCode')

        params = parser.parse_args()

        buttonCode = params.buttonCode

        pipeline = []

        pipeline.append({
            '$addFields': { 
                'application_areas': {
                        '$filter': {  'input': "$application_areas", 'as': "application_area", 'cond': { '$eq': [ "$$application_area.id", buttonCode ] } }
                } 
            }
        })
        pipeline.append({ '$match': { '$expr': { '$gt': [ { '$size': "$application_areas" }, 0 ] } } })
        pipeline.append({ '$project' : { "_id" : 0, 'desc': { '$arrayElemAt': [ "$application_areas", 0 ] } } })

        buttonInfo = mongo.db.documentation.aggregate(pipeline)

        result_info = []
        for result in buttonInfo:
            result_info.append(result)

        return result_info[0]["desc"]["text"]