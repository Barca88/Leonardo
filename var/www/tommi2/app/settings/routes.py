#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.settings import blueprint
from flask import render_template, request, flash
from flask_login import login_required
from app import mongo
from os import path, remove
from werkzeug.security import generate_password_hash
import datetime


UPLOAD_FOLDER = './static/upload/'

@blueprint.route('/')
@login_required
def route_template():
    nome = request.args.get('nome')
    return render_template('settings.html',nome=nome)

@blueprint.route('/adicionar')
@login_required
def route_template_adicionar():
    nome = request.args.get('nome')
    return render_template('addSettings.html',nome=nome)

@blueprint.route('/ver')
@login_required
def route_template_ver():
    settings = mongo.db.settings.find()
    nome = request.args.get('nome')
    return render_template('verSettings.html',settings=settings,nome=nome)

@blueprint.route('/registar', methods=['POST'])
@login_required
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
        return render_template('verSettings.html',settings=settings,nome=nome)


@blueprint.route('/editar/<s>')
@login_required
def route_template_editar(s):
    existe = mongo.db.settings.find_one({"_id":s})
    nome = request.args.get('nome')
    return render_template('editSettings.html', setting=existe,nome=nome)

@blueprint.route('/remover/<s>')
@login_required
def route_template_remover(s):
    nome = request.args.get('nome')
    return render_template('removerTag.html',setting=s,nome=nome)


@blueprint.route('/apagar/<s>')
@login_required
def route_template_apagar(s):
    value = mongo.db.settings.remove({"_id":s})
    settings = mongo.db.settings.find()
    nome = request.args.get('nome')
    return render_template('verSettings.html',settings=settings,nome=nome)

@blueprint.route('/editar/guardar', methods=['POST'])
@login_required
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
    return render_template('verSettings.html',settings=settings,nome=nome)
