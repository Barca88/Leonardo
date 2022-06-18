from flask import Blueprint
from flask import Flask, jsonify, json
from flask_restful import reqparse, Resource
from . import util
from flask import request
from ast import literal_eval
from app import mongo

class Answers(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('log')
        parser.add_argument('answers')
        parser.add_argument('date')
        parser.add_argument('finished')
        parser.add_argument('user')
        parser.add_argument('question')
        parser.add_argument('inquiry_id')

        params = parser.parse_args()

        if 'True' == params.finished:
            answers = literal_eval(params.answers)
            log = literal_eval(params.log)

            values = util.fixAnswersDocument(answers,params.date,params.user,params.question,params.inquiry_id)
            mongo.db.opinions.insert_one(values)
            mongo.db.opinions_logs.insert_one(log)

            return jsonify({
                'status': 'Success',
                'message': 'Answers and log added!'
            })
        else:
            log = literal_eval(params.log)
            mongo.db.opinions_logs.insert_one(log)
            return jsonify({
                'status': 'Success',
                'message': 'Log added!'
            })
