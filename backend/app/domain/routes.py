#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.domain import blueprint
from flask import render_template, request, flash, send_from_directory
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


@blueprint.route('/getDomains', methods=['GET'])
#@admin_required
#@token_required
#@login_required
def route_domain():
    domains= [doc for doc in mongo.db.domains.find()]
    print(domains)
    
    #write_log(user, 'Utilizadores/Gestão', '', 'successfull')
    return json_util.dumps({'domains': domains})
    #return render_template('users.html',users=users,nome=nome)


@blueprint.route('/insert', methods=['POST'])
@admin_required
#@login_required
def route_template_insert():
    print('test')
    print(request)
    _id = request.form.get('id')
    description = request.form.get('description')
    scholarity = request.form.get('scholarity')
    responsible = request.form.get('responsible')
    notes = request.form.get('notes')
    access_type = request.form.get('access_type')
    body = request.form.get('body')
    default_user_level = request.form.get('default_user_level')
    high_performance_factor = request.form.get('high_performance_factor')
    low_performance_factor = request.form.get('low_performance_factor')
    high_skill_factor = request.form.get('high_skill_factor')
    low_skill_factor = request.form.get('low_skill_factor')
    min_questions_number = request.form.get('min_questions_number')
    question_factor = request.form.get('question_factor')
    inserted_by = request.form.get('inserted_by')
    inserted_at = request.form.get('inserted_at')

    mongo.db.domains.insert({"id" :_id , "description": description, "scholarity": scholarity, "responsible": responsible, "notes": notes, "access_type": access_type, "body": body, "default_user_level": default_user_level, "high_performance_factor":high_performance_factor,
    "low_performance_factor" : low_performance_factor, "high_skill_factor": high_skill_factor, "low_skill_factor" : low_skill_factor,
     "min_questions_number": min_questions_number, "question_factor": question_factor, "inserted_by": inserted_by,  "inserted_at": inserted_at })

    print(_id)
    return '1'

