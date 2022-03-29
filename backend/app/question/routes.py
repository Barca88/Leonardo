#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.question import blueprint
from flask import render_template, request, flash, send_from_directory, jsonify
from flask_login import login_required
from app import mongo, token_required, admin_required, photo_auth, write_log
from os import path, remove, rename, replace
from werkzeug.security import generate_password_hash
import datetime
from os.path import join, dirname, realpath
from shutil import copyfile, move
###### este é meu
import json 
import csv
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######
UPLOAD_FOLDER = './static/picss/'





@blueprint.route('/getQuestions', methods=['GET'])
#@admin_required
#@token_required
#@login_required
def question():
    questions= [doc for doc in mongo.db.question.find()]
    print('Getquestions')
    userAdmin = request.args.get('nome')
    if userAdmin:
        write_log(userAdmin, 'Informação Base/Questions', '', 'successfull')
    return json_util.dumps({'questions': questions})
    #return render_template('users.html',users=users,nome=nome)



@blueprint.route('/getQestions/<question>', methods=['GET'])
#@admin_required
#@token_required
#@login_required
def route_domain_get(question):
    #userAdmin = request.args.get('nome')
    print(question)
    existe = mongo.db.question.find_one({"_id":question})
    print(existe)
    question= [doc for doc in mongo.db.question.find()]
    #print(userAdmin)
    return json_util.dumps({'question': existe})



@blueprint.route('/insert', methods=['POST'])
@admin_required
#@login_required
def route_template_insert():
    print("inserir")
    _id = request.form.get('_id')
    print(request.form.get('_id'))
    existe = mongo.db.question.find_one({"_id":_id})
    userAdmin = request.args.get('nome')
    if existe:
        print('Domain ja existe')
        write_log(userAdmin, 'Informação Base/Questoes', 'Adicionar Questao', 'failed')
        return json_util.dumps({'nome': userAdmin,'message':'já existe'})
    else:
        language = request.form.get('language')
        scholarity = request.form.get('scholarity')
        study_cycle = request.form.get('study_cycle')
        domain = request.form.get('domain')
        subdomain = request.form.get('subdomain')
        subsubdomain = request.form.get('subsubdomain')
        difficulty_level = request.form.get('difficulty_level')
        author = request.form.get('author')
        display_mode = request.form.get('display_mode')
        answering_time = request.form.get('answering_time')
        type_ = request.form.get('type')
        precedence = request.form.get('precedence')
        repetitions = request.form.get('repetitions')
        header = request.form.get('header')
        body = request.form.get('body')
        explanation = request.form.get('explanation')
        images = request.form.get('images')
        videos = request.form.get('videos')
        source = request.form.get('source')
        notes = request.form.get('notes')
        status = request.form.get('status')
        inserted_by = request.form.get('inserted_by')
        inserted_at = request.form.get('inserted_at')
        validated_by = request.form.get('validated_by')
        validated_at = request.form.get('validated_at')


        mongo.db.question.insert({"_id" :_id , "language": language, "scholarity": scholarity, "study_cycle": study_cycle, "domain": domain, "subdomain": subdomain, "subsubdomain": subsubdomain, "difficulty_level":difficulty_level,
        "author" : author, "display_mode": display_mode, "answering_time" : answering_time,
        "type_": type_, "precedence": precedence, "repetitions": repetitions,  "header": header,  "body": body,  "explanation": explanation
        ,  "images": images,  "videos": videos,  "source": source,  "notes": notes,  "status": status
        ,  "inserted_by": inserted_by,  "inserted_at": inserted_at,  "validated_by": validated_by,  "validated_at": validated_at })
        write_log(userAdmin, 'Informação Base/Questoes', 'Adicionar Questao', 'successfull')
        return '1'



@blueprint.route('/delete/<question>', methods=['DELETE'])
@admin_required
#@login_required
def route_template_apagar(question):
    print(question)
    mongo.db.question.remove({"_id":question})
    questions = mongo.db.question.find()
    userAdmin = request.args.get('nome')
    write_log(userAdmin, 'Informação Base/question', 'Eliminar question', 'successfull')
    return json_util.dumps({'question': question})



@blueprint.route('/edit', methods=['POST'])
@admin_required
#@login_required
def route_template_editar_guardar():
    print("edit question")
    _id = request.form.get('_id')
    language = request.form.get('language')
    scholarity = request.form.get('scholarity')
    study_cycle = request.form.get('study_cycle')
    domain = request.form.get('domain')
    subdomain = request.form.get('subdomain')
    subsubdomain = request.form.get('subsubdomain')
    difficulty_level = request.form.get('difficulty_level')
    author = request.form.get('author')
    display_mode = request.form.get('display_mode')
    answering_time = request.form.get('answering_time')
    type_ = request.form.get('type')
    precedence = request.form.get('precedence')
    repetitions = request.form.get('repetitions')
    header = request.form.get('header')
    body = request.form.get('body')
    explanation = request.form.get('explanation')
    images = request.form.get('images')
    videos = request.form.get('videos')
    source = request.form.get('source')
    notes = request.form.get('notes')
    status = request.form.get('status')
    inserted_by = request.form.get('inserted_by')
    inserted_at = request.form.get('inserted_at')
    validated_by = request.form.get('validated_by')
    validated_at = request.form.get('validated_at')
    #userAdmin = request.args.get('nome')

    mongo.db.question.update({"_id" :_id} ,{ "language": language, "scholarity": scholarity, "study_cycle": study_cycle, "domain": domain, "subdomain": subdomain, "subsubdomain": subsubdomain, "difficulty_level":difficulty_level,
    "author" : author, "display_mode": display_mode, "answering_time" : answering_time,
    "type_": type_, "precedence": precedence, "repetitions": repetitions,  "header": header,  "explanation": explanation
    ,  "images": images,  "videos": videos,  "source": source,  "notes": notes,  "status": status
    ,  "inserted_by": inserted_by,  "inserted_at": inserted_at,  "validated_by": validated_by,  "validated_at": validated_at })

    


    questions = mongo.db.question.find()
    #write_log(userAdmin, 'Informação Base/Domínios', 'Editar Question', 'successfull')
    return json_util.dumps({'question': question})