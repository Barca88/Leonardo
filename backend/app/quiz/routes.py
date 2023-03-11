#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.quiz import blueprint
from flask_restful                                          import Api
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
from .QuizFolders.evaluation.resources.create_test                     import CreateTest
from .QuizFolders.evaluation.resources.preview_test                    import PreviewTest
from .QuizFolders.evaluation.resources.get_domains                     import GetDomains
from .QuizFolders.evaluation.resources.get_statistics                  import GetStatistics
from .QuizFolders.evaluation.resources.new_evaluation                  import NewEvaluation
from .QuizFolders.evaluation.resources.next_question                   import NextQuestion
from .QuizFolders.evaluation.resources.get_gamification_users          import GetUsers
from .QuizFolders.evaluation.resources.post_gamification_users         import PostUsers
from .QuizFolders.evaluation.resources.get_gamification_domains        import GetDoms
from .QuizFolders.evaluation.resources.get_quizz_monitor_parameters    import GetQuizzParameters
from .QuizFolders.evaluation.resources.get_button_info                 import GetButtonInfo
from .QuizFolders.evaluation.resources.rules                           import Rules
from .QuizFolders.evaluation.resources.rule                            import Rule
from .QuizFolders.accounts.resources.upload_avatar                     import UploadAvatar
from .QuizFolders.accounts.resources.change_password                   import ChangePassword
from .QuizFolders.students.resources.list                              import List
from .QuizFolders.questions.resources.domains_map                      import DomainsMap
from .QuizFolders.questions.resources.get_domains_by_charge            import GetDomainsByCharge
from .QuizFolders.questions.resources.get_subdomains_by_charge         import GetSubdomainsByCharge
from .QuizFolders.inquiries.resources.answers                          import Answers
from .QuizFolders.inquiries.resources.inquiry                          import Inquiry
CORS(blueprint)
#######
UPLOAD_FOLDER = './static/picss/'

internal_api = Api(blueprint)




internal_api.add_resource(CreateTest         , '/evaluation/create_test')
internal_api.add_resource(PreviewTest        , '/evaluation/preview_test/<int:test_id>')
internal_api.add_resource(GetDomains         , '/evaluation/getDomains')
internal_api.add_resource(GetStatistics      , '/evaluation/getStatistics')
internal_api.add_resource(NewEvaluation      , '/evaluation/new')
internal_api.add_resource(NextQuestion       , '/evaluation/next')
internal_api.add_resource(GetQuizzParameters , '/evaluation/quizzParameters')
internal_api.add_resource(GetButtonInfo      , '/evaluation/getButtonInfo')
internal_api.add_resource(Rules              , '/evaluation/rules')
internal_api.add_resource(Rule               , '/evaluation/rules/<int:rule_id>')

# =========== ACCOUNTS ===========
internal_api.add_resource(UploadAvatar  , '/accounts/avatar/upload')
internal_api.add_resource(ChangePassword, '/accounts/password/change')

# =========== STUDENTS ===========
internal_api.add_resource(List, '/students/list')

# =========== QUESTIONS ==========
internal_api.add_resource(DomainsMap, '/questions/domains_map')
internal_api.add_resource(GetDomainsByCharge, '/questions/getDomainsByCharge')
internal_api.add_resource(GetSubdomainsByCharge, '/questions/getSubdomainsByCharge')

# =========== INQUIRIES =========
internal_api.add_resource(Answers,'/inquiries/inquiry_answers')
internal_api.add_resource(Inquiry,'/inquiries/inquiry')

# =========== GAMIFICATION =========
internal_api.add_resource(GetUsers,'/gamification/get_users')
internal_api.add_resource(GetDoms,'/gamification/get_doms')
internal_api.add_resource(PostUsers,'/gamification/post_users')





@blueprint.route('/getQuestions', methods=['GET'])
##admin_required
#@token_required
#@login_required
def question():
    flag = request.args.get('flag')
    if flag == "aproved":
        questions= [doc for doc in mongo.db.question.find({"flag" : "aproved"})]
    if flag == "pending":
        questions= [doc for doc in mongo.db.question.find({"flag" : { "$in":["pending","rejected"]}})]
        
    if flag is None:
        questions = [doc for doc in mongo.db.question.find()]
    users = [doc for doc in mongo.db.users.find({"type" : "Teacher"})]
    domains = [doc for doc in mongo.db.domains.find()]
    print(users)
    print('Getquestions')
    userAdmin = request.args.get('nome')
    if userAdmin:
        write_log(userAdmin, 'Informação Base/Questions', '', 'successfull')
    return json_util.dumps({'questions': questions, 'users': users, 'domains': domains})
    #return render_template('users.html',users=users,nome=nome)



@blueprint.route('/getQuestions/<question>', methods=['GET'])
##admin_required
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


@blueprint.route('/foto/<question>', methods=['GET'])
#@token_required
#@login_required
def route_photo(question):
    print(question)
    _id =question
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    print(question + ' 2 ')
    pathCheck = join(pathPhoto, _id)
    print(question + ' 3 ')
    if  path.exists(pathCheck) :
        print(question + ' 4 ')
        return send_from_directory(pathPhoto, question, mimetype='image/png')
    else :
        print(question + ' 5 ')
        return




@blueprint.route('/insert', methods=['POST'])
#admin_required
#@login_required
def route_template_insert():
    print("inserirquestao")
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
        difficulty_level = request.form.get('difficulty_level')
        author = request.form.get('author')
        display_mode = request.form.get('display_mode')
        answering_time = request.form.get('answering_time')
        type_ = request.form.get('type')
        precedence = request.form.get('precedence')
        repetitions = request.form.get('repetitions')
        header = request.form.get('header')
        body = json.loads(request.form.get('body'))
        explanation = request.form.get('explanation')
        foto = request.files.get('images')
        print('getfoto success')
        print(foto)
        if foto is not None :
            if foto.filename != '':
                print('getfoto success2')
                
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + _id)

        videos = request.form.get('videos')
        source = request.form.get('source')
        notes = request.form.get('notes')
        status = request.form.get('status')
        inserted_by = request.form.get('inserted_by')
        inserted_at = request.form.get('inserted_at')
        validated_by = request.form.get('validated_by')
        validated_at = request.form.get('validated_at')
        flag = request.form.get('flag')

        print('A inserir questao - app quiz')
        mongo.db.question.insert({"_id" :_id , "language": language, "scholarity": scholarity, "study_cycle": study_cycle, "domain": domain, "subdomain": subdomain, "difficulty_level":difficulty_level,
        "author" : author, "display_mode": display_mode, "answering_time" : answering_time,
        "type_": type_, "precedence": precedence, "repetitions": repetitions,  "header": header,  "body": body,  "explanation": explanation
        ,  #"images": images,
          "videos": videos,  "source": source,  "notes": notes,  "status": status
        ,  "inserted_by": inserted_by,  "inserted_at": inserted_at,  "validated_by": validated_by,  "validated_at": validated_at, "flag":flag })
        write_log(userAdmin, 'Informação Base/Questoes', 'Adicionar Questao', 'successfull')
        return '1'




@blueprint.route('/delete/<question>', methods=['DELETE'])
#admin_required
#@login_required
def route_template_apagar(question):
    print(question)
    mongo.db.question.remove({"_id":question})
    question = mongo.db.question.find()
    userAdmin = request.args.get('nome')
    write_log(userAdmin, 'Informação Base/question', 'Eliminar question', 'successfull')
    return json_util.dumps({'question': question})



@blueprint.route('/edit', methods=['POST'])
#admin_required
#@login_required
def route_template_editar_guardar():
    print("edit question")
    _id = request.form.get('_id')
    language = request.form.get('language')
    scholarity = request.form.get('scholarity')
    study_cycle = request.form.get('study_cycle')
    domain = request.form.get('domain')
    subdomain = request.form.get('subdomain')
    difficulty_level = request.form.get('difficulty_level')
    author = request.form.get('author')
    display_mode = request.form.get('display_mode')
    answering_time = request.form.get('answering_time')
    type_ = request.form.get('type')
    precedence = request.form.get('precedence')
    repetitions = request.form.get('repetitions')
    header = request.form.get('header')
    body = json.loads(request.form.get('body'))
    explanation = request.form.get('explanation')
    foto = request.files.get('images')
    if foto is not None :
        if foto.filename != '':
                print('getfoto success2')
                
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + _id)
    videos = request.form.get('videos')
    source = request.form.get('source')
    notes = request.form.get('notes')
    status = request.form.get('status')
    inserted_by = request.form.get('inserted_by')
    inserted_at = request.form.get('inserted_at')
    validated_by = request.form.get('validated_by')
    validated_at = request.form.get('validated_at')
    flag = request.form.get('flag')
    #userAdmin = request.args.get('nome')

    mongo.db.question.update({"_id" :_id} ,{ "language": language, "scholarity": scholarity, "study_cycle": study_cycle, "domain": domain, "subdomain": subdomain, "difficulty_level":difficulty_level,
    "author" : author, "display_mode": display_mode, "answering_time" : answering_time,"body": body,
    "type_": type_, "precedence": precedence, "repetitions": repetitions,  "header": header,  "explanation": explanation
    ,   "videos": videos,  "source": source,  "notes": notes,  "status": status
    ,  "inserted_by": inserted_by,  "inserted_at": inserted_at,  "validated_by": validated_by,  "validated_at": validated_at, "flag":flag })

    


    
    #write_log(userAdmin, 'Informação Base/Domínios', 'Editar Question', 'successfull')
    return json_util.dumps({'question': 'Success'})