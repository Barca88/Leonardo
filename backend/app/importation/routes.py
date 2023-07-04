from itertools import count
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
    user = request.args.get('nome')
    write_log(user, 'Verificação/Dashboard', 'Sem filtros', 'successfull')
    questions = mongo.db.question.find({'imported': True})
    return json_util.dumps({'questions': questions})

@blueprint.route('/imported_questions/statsByAuthor/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupAuthor.yml')
def lookupAuthor(id):
    user = request.args.get('nome')
    write_log(user, 'Verificação/Dashboard', 'Aplicar filtro', 'successfull')
    questions = mongo.db.question.find({'author':id.replace(","," "),'imported': True})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions/statsByDomain/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupDomain.yml')
def lookupDomain(id):
    user = request.args.get('nome')
    write_log(user, 'Verificação/Dashboard', 'Aplicar filtro', 'successfull')
    questions = mongo.db.question.find({'domain':id.replace(","," "), 'imported': True})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions/statsByBoth/<author>/<domain>',methods=['GET']) # check
@swag_from('docs/questions/lookupBoth.yml')
def lookupBoth(author,domain):
    user = request.args.get('nome')
    write_log(user, 'Verificação/Dashboard', 'Aplicar filtro', 'successfull')
    questions = mongo.db.question.find({'domain':domain.replace(","," "),'author': author.replace(","," "), 'imported': True})
    return json_util.dumps({'questions': questions})


@blueprint.route('/imported_questions',methods=['POST']) # check
@swag_from('docs/questions/insertQuestion.yml')
def insertQuestion():
    question = request.get_json(force=True)
    exist = mongo.db.question.find_one({"_id":question['_id']})
    if exist:
        return json_util.dumps({'message': "error"})
    print('A inserir questao - app importation')
    mongo.db.question.insert_one(question)
    return jsonify('Inserted new question')

@blueprint.route('/imported_questions/<id>',methods=['PUT']) # check
@swag_from('docs/questions/editQuestion.yml')
def editQuestion(id):
    user = request.args.get('nome')
    question = request.get_json(force=True)
    print(question['flag'])
    if question['flag'] == "rejected":
        write_log(user, 'Verificação/Verificação de Questões', 'Rejeitar Questão', 'successfull')
    if question['flag'] == "aproved":
        mongo.db.question.find_one_and_update({'_id':id},{'$set': {'validated_at':question['validated_at'], 'validated_by':question['validated_by']}},upsert=True)
        write_log(user, 'Verificação/Verificação de Questões', 'Aprovar Questão', 'successfull')
    mongo.db.question.find_one_and_update({'_id':id},{'$set': {'flag':question['flag']}},upsert=True)
    return jsonify('Questão actualizada com sucesso ...')

@blueprint.route('/remove_questions/<id>',methods=['PUT']) # check
@swag_from('docs/questions/editQuestion.yml')
def removeQuestion(id):
    user = request.args.get('nome')
    mongo.db.question.remove({"_id":id})
    write_log(user, 'Verificação/Verificação de Questões', 'Remover Questão', 'successfull')
    questions= [doc for doc in mongo.db.question.find({"flag" : { "$in":["pending","rejected"]}})]
    print(questions)
    return json_util.dumps({'questions': questions})

#########################################################

####################### ERRORS ########################

@blueprint.route('/imported_errors',methods=['GET']) #check
@swag_from('docs/errors/listErrors.yml')
def listErrors():
    user = request.args.get('nome')
    if user:
        write_log(user, 'Verificação/Verificação de Erros', '', 'successfull')
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
    user = request.args.get('nome')
    write_log(user, 'Verificação/Verificação de Erros', 'Limpar Erros', 'successfull')
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
    user = request.args.get('nome')
    count = request.args.get('count')
    if count == "0":
        write_log(user, 'Verificação/Importação de Questões', 'Importar Questões', 'successfull')
    else:
        write_log(user, 'Verificação/Importação de Questões', 'Importar Questões', 'failed')
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
       #path = os.getcwd() + "\\app\importation\scripts\mkleonardo.py" #Windows
       path = os.getcwd() + "//app/importation/scripts/mkleonardo.py" #Linux
       print(path)
       result = subprocess.run(["python", path],stdout = subprocess.PIPE, input=content)
       print("----------------------------------------------")
       print(result)
       # Return the json
       answer = "[" + result.stdout.decode('utf-8') + "]"
       print("----------------------------------------------")
       print(answer)

    return answer