from flask_restful import Resource
from app           import mongo

class PreviewTest(Resource):
    def get(self, test_id):
        return mongo.db.tests.find_one({ 'id': test_id })
