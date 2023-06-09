#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.settings import blueprint
from flask import render_template, request, flash
from flask_login import login_required
from app import mongo, token_required, admin_required
from os import path, remove
from werkzeug.security import generate_password_hash
import datetime
###### este é meu
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######

UPLOAD_FOLDER = './static/upload/'

@blueprint.route('/')
@token_required
#@login_required
def route_template():
    nome = request.args.get('nome')
    return render_template('settings.html',nome=nome)

@blueprint.route('/adicionar')
@token_required
#@login_required
def route_template_adicionar():
    nome = request.args.get('nome')
    return render_template('addSettings.html',nome=nome)

@blueprint.route('/ver', methods=['GET'])
@token_required
#@login_required
def route_template_ver():
    settings = mongo.db.settings.find()
    nome = request.args.get('nome')
    return json_util.dumps({'nome': nome,'settings':settings})

@blueprint.route('/registar', methods=['POST'])
@admin_required
#@login_required
def route_template_registar():
    elemento = request.form.get('elemento')
    existe = mongo.db.settings.find_one({"_id":elemento})
    nome = request.args.get('nome')
    if existe:
        flash('ERRO: Elemento ja existe.')
        return render_template('addSettings.html',nome=nome)
    else:
        desc = request.form.get('desc')
        wac = request.form.get('wac')
        tag = request.form.get('tag')
        exemplo = request.form.get('exemplo')
        procurar = request.form.get('procurar')
        if procurar == 'sim':
            procura = True
        else:
            procura = False
        value = mongo.db.settings.insert({"_id":elemento,"desc":desc,"wac":wac,"tag":tag,"exemplo":exemplo,"procura":procura})
        settings = mongo.db.settings.find()
        return json_util.dumps({'nome': nome,'settings':settings})


@blueprint.route('/editar/<s>')
@admin_required
#@login_required
def route_template_editar(s):
    existe = mongo.db.settings.find_one({"_id":s})
    nome = request.args.get('nome')
    return render_template('editSettings.html', setting=existe,nome=nome)

@blueprint.route('/remover/<s>')
@admin_required
#@login_required
def route_template_remover(s):
    nome = request.args.get('nome')
    return render_template('removerTag.html',setting=s,nome=nome)


@blueprint.route('/apagar/<s>', methods=['GET'])
@admin_required
#@login_required
def route_template_apagar(s):
    value = mongo.db.settings.remove({"_id":s})
    settings = mongo.db.settings.find()
    nome = request.args.get('nome')
    return json_util.dumps({'nome': nome,'settings':settings})

@blueprint.route('/editar/guardar', methods=['POST'])
@admin_required
#@login_required
def route_template_editar_guardar():
    nome = request.args.get('nome')
    elemento = request.form.get('elemento')
    desc = request.form.get('desc')
    wac = request.form.get('wac')
    tag = request.form.get('tag')
    exemplo = request.form.get('exemplo')
    procurar = request.form.get('procurar')
    if procurar == 'sim':
        procura = True
    else:
        procura = False 
    value = mongo.db.settings.update({"_id":elemento},{"$set":{"desc":desc,"wac":wac,"tag":tag,"exemplo":exemplo,"procura":procura}})    
    settings = mongo.db.settings.find()
    return json_util.dumps({'nome': nome,'settings':settings})
