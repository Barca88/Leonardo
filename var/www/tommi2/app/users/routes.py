#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.users import blueprint
from flask import render_template, request, flash
from flask_login import login_required
from app import mongo
from os import path, remove
from werkzeug.security import generate_password_hash
import datetime
from os.path import join, dirname, realpath
from shutil import copyfile

UPLOAD_FOLDER = './static/pics/'

@blueprint.route('/users')
@login_required
def route_template():
    users = mongo.db.users.find()
    nome = request.args.get('nome')
    return render_template('users.html',users=users,nome=nome)


@blueprint.route('/adicionar')
@login_required
def route_template_adicionar():
    nome = request.args.get('nome')
    return render_template('registar.html',nome=nome)

@blueprint.route('/registar', methods=['POST'])
@login_required
def route_template_registar():
    username = request.form.get('username')
    existe = mongo.db.users.find_one({"_id":username})
    nome = request.args.get('nome')
    if existe:
        flash('ERRO: Username já escolhido. Por favor escolha outro...')
        return render_template('registar.html',nome=nome)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        encryptPass = generate_password_hash(password)
        tipo = request.form.get('tipo')
        pai = request.form.get('pai')
        mae = request.form.get('mae')
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/pics/', "default.png") 
                upload_path = join(dirname(realpath(__file__)), 'static/pics/', username)
                copyfile(src, upload_path)
        obs = request.form.get('obs')
        value = mongo.db.users.insert({"_id":username,"nome":name,"email":email,"password":encryptPass,"tipo":tipo,"pai":pai,"mae":mae,"data":data,"obs":obs})
        users = mongo.db.users.find()
        return render_template('users.html',users=users,nome=nome)


@blueprint.route('/ver/<user>')
@login_required
def route_template_ver(user):
    nome = request.args.get('nome')
    existe = mongo.db.users.find_one({"_id":user})
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    return render_template('view.html', user=existe, foto=foto,nome=nome)


@blueprint.route('/editar/<user>')
@login_required
def route_template_editar(user):
    existe = mongo.db.users.find_one({"_id":user})
    nome = request.args.get('nome')
    return render_template('edit.html', user=existe,nome=nome)


@blueprint.route('/remover/<user>')
@login_required
def route_template_remover(user):
    nome = request.args.get('nome')
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    return render_template('remover.html',user=user,foto=foto,nome=nome)


@blueprint.route('/apagar/<user>')
@login_required
def route_template_apagar(user):
    value = mongo.db.users.remove({"_id":user})
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    if path.exists(upload_path): 
        remove(upload_path)
    users = mongo.db.users.find()
    nome = request.args.get('nome')
    return render_template('users.html',users=users,nome=nome)

@blueprint.route('/editar/guardar', methods=['POST'])
@login_required
def route_template_editar_guardar():
    username = request.form.get('username')
    nome = request.form.get('name')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    pai = request.form.get('pai')
    mae = request.form.get('mae')
    obs = request.form.get('obs')
    nome = request.args.get('nome')
    if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
    password = request.form.get('password')
    if password:
        encryptPass = generate_password_hash(password)
        value = mongo.db.users.update({"_id":username},{"nome":nome,"email":email,"password":encryptPass,"tipo":tipo,"pai":pai,"mae":mae,"obs":obs})
    else:
        value = mongo.db.users.update({"_id":username},{"$set":{"nome":nome,"email":email,"tipo":tipo,"pai":pai,"mae":mae,"obs":obs}})    
    users = mongo.db.users.find()
    return render_template('users.html',users=users,nome=nome)