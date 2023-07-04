#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.domain import blueprint
from app.question.routes import route_template_apagar
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





@blueprint.route('/getDomains', methods=['GET'])
####@admin_required
#@token_required
#@login_required
def route_domain():
    domains= [doc for doc in mongo.db.domains.find()]
    users = [doc for doc in mongo.db.users.find({"type" : "Teacher"})]
    userAdmin = request.args.get('nome')
    if userAdmin:  
        write_log(userAdmin, 'Informação Base/Domínios', '', 'successfull')
    return json_util.dumps({'domains': domains, 'users': users})
    #return render_template('users.html',users=users,nome=nome)



@blueprint.route('/getDomains/<domain>', methods=['GET'])
###@admin_required
#@token_required
#@login_required
def route_domain_get(domain):
    #userAdmin = request.args.get('nome')
    print(domain)
    existe = mongo.db.domains.find_one({"_id":domain})
    print(existe)
    domains= [doc for doc in mongo.db.domains.find()]
    #print(userAdmin)
    return json_util.dumps({'domain': existe})



@blueprint.route('/insert', methods=['POST'])
##@admin_required
#@login_required
def route_template_insert():
    print("inserir")
    _id = request.form.get('_id')
    print(request.form.get('body'))
    existe = mongo.db.domains.find_one({"_id":_id})
    userAdmin = request.args.get('nome')
    if existe:
        print('Domain ja existe')
        write_log(userAdmin, 'Informação Base/Domínios', 'Adicionar Domínio', 'failed')
        return json_util.dumps({'nome': userAdmin,'message':'já existe'})
    else:
        description = request.form.get('description')
        scholarity = request.form.get('scholarity')
        responsible = request.form.get('responsible')
        notes = request.form.get('notes')
        access_type = request.form.get('access_type')

        body = json.loads(request.form.get('body'))
        
        default_user_level = request.form.get('default_user_level')
        high_performance_factor = request.form.get('high_performance_factor')
        low_performance_factor = request.form.get('low_performance_factor')
        high_skill_factor = request.form.get('high_skill_factor')
        low_skill_factor = request.form.get('low_skill_factor')
        min_questions_number = request.form.get('min_questions_number')
        question_factor = request.form.get('question_factor')
        backlog_factor = request.form.get('backlog_factor')
        inserted_at = request.form.get('inserted_at')

        mongo.db.domains.insert({"_id" :_id , "domain" :_id, "description": description, "scholarity": scholarity, "responsible": responsible, "notes": notes, "access_type": access_type, "body": body, "default_user_level": default_user_level, "high_performance_factor":high_performance_factor,
        "low_performance_factor" : low_performance_factor, "high_skill_factor": high_skill_factor, "low_skill_factor" : low_skill_factor,
        "min_questions_number": min_questions_number, "question_factor": question_factor, "inserted_by": userAdmin,  "inserted_at": inserted_at, "backlog_factor": backlog_factor})
        
        imp = request.args.get('importation')
        print(imp)
        if imp != 'imp':
            write_log(userAdmin, 'Informação Base/Domínios', 'Adicionar Domínio', 'successfull')
        return '1'



@blueprint.route('/apagar/<domain>', methods=['DELETE'])
##@admin_required
#@login_required
def route_template_apagar1(domain):
    questoes = mongo.db.question.find({"domain":domain})
    for q in questoes:
        print(q)
        question = json.loads(json.dumps(q))
        route_template_apagar(question['_id'])
    
    mongo.db.domains.remove({"_id":domain})
    domains = mongo.db.domains.find()
    userAdmin = request.args.get('nome')
    write_log(userAdmin, 'Informação Base/Domínios', 'Eliminar Domínio', 'successfull')
    return json_util.dumps({'Domains': domains})



@blueprint.route('/editar', methods=['POST'])
##@admin_required
#@login_required
def route_template_editar_guardar():
    print("editar")
    _id = request.form.get('_id')
    domain = _id
    print(request.form.get('body'))
    description = request.form.get('description')
    scholarity = request.form.get('scholarity')
    responsible = request.form.get('responsible')
    notes = request.form.get('notes')
    access_type = request.form.get('access_type')
    body = json.loads(request.form.get('body'))
    default_user_level = request.form.get('default_user_level')
    high_performance_factor = request.form.get('high_performance_factor')
    low_performance_factor = request.form.get('low_performance_factor')
    high_skill_factor = request.form.get('high_skill_factor')
    low_skill_factor = request.form.get('low_skill_factor')
    min_questions_number = request.form.get('min_questions_number')
    question_factor = request.form.get('question_factor')
    backlog_factor = request.form.get('backlog_factor')
    inserted_by = request.form.get('inserted_by')
    inserted_at = request.form.get('inserted_at')
    userAdmin = request.args.get('nome')

    mongo.db.domains.update({"_id":_id},{"$set":{"description":description,"domain": domain,"backlog_factor":backlog_factor, "scholarity":scholarity,"responsible":responsible,"notes":notes,"access_type":access_type,"default_user_level":default_user_level,
    "high_performance_factor":high_performance_factor,"low_performance_factor":low_performance_factor,"high_skill_factor":high_skill_factor,"low_skill_factor":low_skill_factor,"body":body,
    "min_questions_number":min_questions_number,"question_factor":question_factor,"inserted_by":inserted_by,"inserted_at":inserted_at}})


    domains = mongo.db.domains.find()
    imp = request.args.get('importation')
    print(imp)
    if imp != 'imp':
        write_log(userAdmin, 'Informação Base/Domínios', 'Editar Domínio', 'successfull')
    return json_util.dumps({'Domains': domains})