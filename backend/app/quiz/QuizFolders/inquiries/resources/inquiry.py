from flask import Blueprint
from flask import Flask, jsonify, json
from flask_restful import reqparse, Resource
from ast import literal_eval
from . import util

class Inquiry(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('inquiry')

        params = parser.parse_args()

        data = util.findInquiry(params.inquiry)

        return jsonify({
            'status': 'success',
            'questions': data['properties'],
            'comments': data['text'],
            'inquiry_id': data['inquiry_id'],
            'utility': data['utility'],
            'type': data.get('module', '')
            })

