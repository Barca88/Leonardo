from app.importation import blueprint
from flask import render_template, request, flash, send_from_directory
from flask_login import login_required
from app import mongo, token_required, admin_required, photo_auth, write_log
from os import path, remove, rename, replace
from werkzeug.security import generate_password_hash
from flask import Flask, request,jsonify,Response
from flasgger import swag_from, Swagger
from flask_cors import CORS, cross_origin
from bson import ObjectId
import datetime
from os.path import join, dirname, realpath
from shutil import copyfile, move
###### este é meu
import json 
import csv
from bson import json_util
from flask_cors import CORS, cross_origin
import os
import subprocess
import settings
CORS(blueprint)

#leonardo.imported_questions

####################### QUESTIONS ########################
@blueprint.route('/imported_questions', methods=['GET']) # check
@swag_from('docs/questions/listQuestions.yml')
def listQuestions():
    questions = mongo.db.question.find()
    return json_util.dumps({'questions': questions})

@blueprint.route('/imported_questions/statsByAuthor/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupAuthor.yml')
def lookupAuthor(id):
    questions = mongo.db.question.find({'author':id.replace(","," ")})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions/statsByDomain/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupDomain.yml')
def lookupDomain(id):
    questions = mongo.db.question.find({'domain':id.replace(","," ")})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions/statsByBoth/<author>/<domain>',methods=['GET']) # check
@swag_from('docs/questions/lookupBoth.yml')
def lookupBoth(author,domain):
    questions = mongo.db.question.find({'domain':domain.replace(","," "),'author': author.replace(","," ")})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions',methods=['POST']) # check
@swag_from('docs/questions/insertQuestion.yml')
def insertQuestion():
    question = request.get_json(force=True)
    exist = mongo.db.question.find_one({"_id":question['_id']})
    if exist:
        return json_util.dumps({'message': "error"})
    mongo.db.question.insert_one(question)
    return jsonify('Inserted new question')

@blueprint.route('/imported_questions/<id>',methods=['PUT']) # check
@swag_from('docs/questions/editQuestion.yml')
def editQuestion(id):
    question = request.get_json(force=True)
    mongo.db.question.find_one_and_update({'_id':id},{'$set': {'flag':question['flag']}},upsert=True)
    return jsonify('Questão actualizada com sucesso ...')

#########################################################

####################### ERRORS ########################

@blueprint.route('/imported_errors',methods=['GET']) #check
@swag_from('docs/errors/listErrors.yml')
def listErrors():
    errors = mongo.db.imported_errors.find()
    return json_util.dumps({'errors': errors})

@blueprint.route('/imported_errors',methods=['POST'])  #check
@swag_from('docs/errors/insertError.yml')
def insertError():
    error = request.get_json(force=True)
    error['id'] = len(list(mongo.db.imported_errors.find()))
    print(error)
    mongo.db.imported_errors.insert_one(error)
    return jsonify('Inserted new error')

@blueprint.route('/errorCleanse', methods=['GET'])
@token_required
def route_error_Cleanse():
    mongo.db.imported_errors.drop()
    reqs= [doc for doc in mongo.db.imported_errors.find()]
    return json_util.dumps({'history': reqs})

#########################################################


####################### INFOS ########################

@blueprint.route('/imported_info',methods=['GET']) # check
@swag_from('docs/info/listInfos.yml')
def listInfos():
    info = mongo.db.imported_info.find()
    return json_util.dumps({'info': info})

@blueprint.route('/imported_info',methods=['POST']) # check
@swag_from('docs/info/insertInfo.yml')
def insertInfo():
    info = request.get_json(force=True)
    mongo.db.imported_info.insert_one(info)
    return jsonify('Inserted new info')

#########################################################


@blueprint.route('/text',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def text():
    """Importação de Questões.
    Importação das questões num formato anotado (.leo)
    ---
    tags:
      - Questões
    requestBody:
        description: Questão a publicar
        required: true
        content:
            text/plain:
                schema:
                    $ref: '#/definitions/Questão'
    definitions:
      Questão:
          type: object
          properties:
            question:
              type: file
              required: true

    responses:
      200:
        description: Importação da questão realizada com sucesso .

      500:
        description: Erro .
    """

    if request.method == 'POST':
       # Store .leo text and get it ready to be converted
       content = request.get_data()
       # Get path of program to be ran
       path = os.getcwd() + "/scripts/mkleonardo.py"
       result = subprocess.run(["python3", path],stdout = subprocess.PIPE, input=content)
       # Return the json
       answer = "[" + result.stdout.decode('utf-8') + "]"

    return answer