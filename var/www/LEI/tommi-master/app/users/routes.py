#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.users import blueprint
from flask import render_template, request, flash, send_from_directory
from flask_login import login_required
from app import mongo, token_required, admin_required, photo_auth
from os import path, remove, rename, replace
from werkzeug.security import generate_password_hash
import datetime
from os.path import join, dirname, realpath
from shutil import copyfile, move
###### este é meu
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######
UPLOAD_FOLDER = './static/pics/'


@blueprint.route('/users', methods=['GET'])
@admin_required
#@token_required
#@login_required
def route_users():
    #users = mongo.db.users.find()
    users= [doc for doc in mongo.db.users.find()]
    nome = request.args.get('nome')
    return json_util.dumps({'users': users, 'nome': nome})
    #return render_template('users.html',users=users,nome=nome)


@blueprint.route('/adicionar')
@admin_required
#@login_required
def route_template_adicionar():
    nome = request.args.get('nome')
    return render_template('registar.html',nome=nome)

@blueprint.route('/registar', methods=['POST'])
@admin_required
#@login_required
def route_template_registar():
    username = request.form.get('username')
    existe = mongo.db.users.find_one({"_id":username})
    nome = request.args.get('nome')
    if existe:
        #flash('ERRO: Username já escolhido. Por favor escolha outro...')
        #return render_template('registar.html',nome=nome)
        return json_util.dumps({'nome': nome,'message':'já existe'})
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        encryptPass = generate_password_hash(password)
        tipo = request.form.get('tipo')
        universidade = request.form.get('universidade')
        departamento = request.form.get('departamento')
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/pics/', username + ".png") 
                upload_path = join(dirname(realpath(__file__)), 'static/pics/', username + ".png")
                copyfile(src, upload_path)
        if 'curriculo' in request.files:
            curriculo = request.files['curriculo']
            if curriculo.filename != '':
                curriculo.filename = username
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/')
                curriculo.save(upload_path2 + curriculo.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/curriculo/', username + ".pdf") 
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', username + ".pdf")
                copyfile(src, upload_path2)
        obs = request.form.get('obs')
        value = mongo.db.users.insert({"_id":username,"nome":name,"email":email,"password":encryptPass,"tipo":tipo,"universidade":universidade,"departamento":departamento,"data":data,"obs":obs})
        users = mongo.db.users.find()
        return json_util.dumps({'nome': nome})


@blueprint.route('/ver/<user>', methods=['GET'])
@admin_required
#@login_required
def route_template_ver(user):
    nome = request.args.get('nome')
    existe = mongo.db.users.find_one({"_id":user})
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user)
    print("path: " + upload_path)
    print("name: " + user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    if path.exists(upload_path2):
        curriculo = user
    else:
        curriculo = "default.png"
    return json_util.dumps({'user': existe, 'foto':upload_path, 'curriculo':upload_path2, 'nome':nome})



###########################################
@blueprint.route('/foto/<user>', methods=['GET'])
@token_required
def route_photo(user):
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if photo_auth (request, user) and path.exists(pathCheck) :
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

@blueprint.route('/foto/atualizar/<user>', methods=['POST'])
@token_required
def route_foto_atualizar(user):
    if 'foto' in request.files:
        foto = request.files['foto']
        upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
        if path.exists(upload_path): 
            remove(upload_path)
        if foto.filename != '':
            foto.filename = user
            upload_path2 = join(dirname(realpath(__file__)), 'static/pics/')
            foto.save(upload_path2 + foto.filename)
        else:
            src = join(dirname(realpath(__file__)), 'static/pics/', user + ".png") 
            upload_path2 = join(dirname(realpath(__file__)), 'static/pics/', user + ".png")
            copyfile(src, upload_path2)

    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if photo_auth (request, user) and path.exists(pathCheck) :
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')



##########################################
@blueprint.route('/curriculo/<user>', methods=['GET'])
@token_required
def route_cur(user):
    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
    print (pathC)
    print (user)
    if photo_auth (request, user) :    
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')

@blueprint.route('/curriculo/atualizar/<user>', methods=['POST'])
@token_required
def route_cur_atualizar(user):
    if 'curriculo' in request.files:
        curriculo = request.files['curriculo']
        upload_path = join(dirname(realpath(__file__)), 'static/curriculo/', user)
        if path.exists(upload_path): 
            remove(upload_path)
        if curriculo.filename != '':
            curriculo.filename = user
            upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/')
            curriculo.save(upload_path2 + curriculo.filename)
        else:
            src = join(dirname(realpath(__file__)), 'static/curriculo/', user + ".pdf") 
            upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user + ".pdf")
            copyfile(src, upload_path2)

    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
    if photo_auth (request, user) :
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')
##########################################



@blueprint.route('/editar/<user>')
@admin_required
#@login_required
def route_template_editar(user):
    existe = mongo.db.users.find_one({"_id":user})
    nome = request.args.get('nome')
    return json_util.dumps({'user': existe, 'nome': nome})


@blueprint.route('/remover/<user>')
@admin_required
#@login_required
def route_template_remover(user):
    nome = request.args.get('nome')
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    return render_template('remover.html',user=user,foto=foto,nome=nome)


@blueprint.route('/apagar/<user>')
@admin_required
#@login_required
def route_template_apagar(user):
    value = mongo.db.users.remove({"_id":user})
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user)
    if path.exists(upload_path): 
        remove(upload_path)
    if path.exists(upload_path2): 
        remove(upload_path2)
    users = mongo.db.users.find()
    nome = request.args.get('nome')
    return json_util.dumps({'users': users, 'nome': nome})

@blueprint.route('/editar/guardar', methods=['POST'])
@admin_required
#@login_required
def route_template_editar_guardar():
    username = request.form.get('username')
    nome = request.form.get('name')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    universidade = request.form.get('universidade')
    departamento = request.form.get('departamento')
    obs = request.form.get('obs')
    nome2 = request.args.get('nome')
    if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
    if 'curriculo' in request.files:
            curriculo = request.files['curriculo']
            if curriculo.filename != '':
                curriculo.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/curriculo/')
                curriculo.save(upload_path + curriculo.filename)
    password = request.form.get('password')
    if password:
        value = mongo.db.users.update({"_id":username},{"nome":nome,"email":email,"password":password,"tipo":tipo,"universidade":universidade,"departamento":departamento,"obs":obs})
    else:
        value = mongo.db.users.update({"_id":username},{"$set":{"nome":nome,"email":email,"tipo":tipo,"universidade":universidade,"departamento":departamento,"obs":obs}})    
    users = mongo.db.users.find()
    return json_util.dumps({'users': users, 'nome': nome2})

###### PEDIDOS ######

@blueprint.route('/pedidos', methods=['GET'])
@admin_required
#@token_required
#@login_required
def route_pedidos():
    pedidos= [doc for doc in mongo.db.pedidos.find()]
    nome = request.args.get('nome')
    return json_util.dumps({'pedidos': pedidos, 'nome': nome})

@blueprint.route('/pedidos/registar', methods=['POST'])
#@admin_required
#@login_required
def route_template_registar_pedido():
    username = request.form.get('username')
    existeU = mongo.db.users.find_one({"_id":username})
    existeP = mongo.db.pedidos.find_one({"_id":username})
    nome = request.args.get('nome')
    if existeU or existeP:
        #flash('ERRO: Username já escolhido. Por favor escolha outro...')
        #return render_template('registar.html',nome=nome)
        return json_util.dumps({'nome': nome,'message':'já existe'})
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        encryptPass = generate_password_hash(password)
        tipo = request.form.get('tipo')
        universidade = request.form.get('universidade')
        departamento = request.form.get('departamento')
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/')
                foto.save(upload_path + foto.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/picsPedidos/', username + ".png") 
                upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', username + ".png")
                copyfile(src, upload_path)
        if 'curriculo' in request.files:
            curriculo = request.files['curriculo']
            if curriculo.filename != '':
                curriculo.filename = username
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/')
                curriculo.save(upload_path2 + curriculo.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', username + ".pdf") 
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', username + ".pdf")
                copyfile(src, upload_path)
        obs = request.form.get('obs')
        value = mongo.db.pedidos.insert({"_id":username,"nome":name,"email":email,"password":encryptPass,"tipo":tipo,"universidade":universidade,"departamento":departamento,"data":data,"obs":obs})
        pedidos = mongo.db.pedidos.find()
        return json_util.dumps({'nome': nome})


@blueprint.route('/pedidos/ver/<pedido>', methods=['GET'])
@admin_required
#@login_required
def route_template_ver_pedido(pedido):
    nome = request.args.get('nome')
    existe = mongo.db.pedidos.find_one({"_id":pedido})
    upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', pedido)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', pedido)
    print("path: " + upload_path)
    print("name: " + pedido)
    if path.exists(upload_path):
        foto = pedido
    else:
        foto = "default.png"
    if path.exists(upload_path2):
        curriculo = pedido
    else:
        curriculo = "default.png"
    return json_util.dumps({'pedido': existe, 'foto':upload_path, 'curriculo':upload_path2, 'nome':nome})



###########################################
@blueprint.route('/pedidos/foto/<pedido>', methods=['GET'])
@token_required
def route_photo_pedido(pedido):
    pathPhoto = join(dirname(realpath(__file__)), 'static/picsPedidos/')
    pathCheck = join(pathPhoto, pedido)
    if photo_auth (request, pedido) and path.exists(pathCheck) :  
        return send_from_directory(pathPhoto, pedido, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

##########################################
@blueprint.route('/pedidos/curriculo/<pedido>', methods=['GET'])
@token_required
def route_cur_pedido(pedido):
    pathC = join(dirname(realpath(__file__)), 'static/curriculoPedidos/')
    print (pathC)
    print (pedido)
    if photo_auth (request, pedido) :    
        return send_from_directory(pathC, pedido,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "Rafiki",mimetype='application/pdf')
##########################################

@blueprint.route('/pedidos/apagar/<pedido>')
@admin_required
#@login_required
def route_template_apagar_pedido(pedido):
    value = mongo.db.pedidos.remove({"_id":pedido})
    upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', pedido)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', pedido)
    if path.exists(upload_path): 
        remove(upload_path)
    if path.exists(upload_path2): 
        remove(upload_path2)
    pedidos = mongo.db.pedidos.find()
    nome = request.args.get('nome')
    return json_util.dumps({'pedidos': pedidos, 'nome': nome})

@blueprint.route('/pedidos/mover/<pedido>')
@admin_required
#@login_required
def route_template_mover_pedido(pedido):
    value1 = mongo.db.pedidos.find_one({"_id": pedido})
    value2 = mongo.db.users.insert(value1)
    value3 = mongo.db.pedidos.remove({"_id":pedido})
    upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', pedido)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', pedido)
    if path.exists(upload_path):
        new_path = join(dirname(realpath(__file__)), 'static/pics/', pedido)
        rename(upload_path, new_path)
    if path.exists(upload_path2):
        new_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', pedido)
        rename(upload_path2, new_path2)
    pedidos = mongo.db.pedidos.find()
    nome = request.args.get('nome')
    return json_util.dumps({'pedidos': pedidos, 'nome': nome})



@blueprint.route('/active', methods=['GET'])
@token_required
def route_active():
    users= [doc for doc in mongo.db.activeUsers.find()]
    date = datetime.datetime.now()
    date = date - datetime.timedelta(minutes = 15)
    ret=[]
    for u in users:
        if datetime.datetime.strptime(u['stamp'],'%Y-%m-%d %H:%M:%S.%f') > date :
            ret.append(u)
    return json_util.dumps({'users': ret})
    #return render_template('users.html',users=users,nome=nome)


@blueprint.route('/history', methods=['GET'])
@token_required
def route_history():
    reqs= [doc for doc in mongo.db.history.find()]
    return json_util.dumps({'reqs': reqs})

@blueprint.route('/historyCleanse', methods=['GET'])
@token_required
def route_historyCleanse():
    mongo.db.history.drop()
    reqs= [doc for doc in mongo.db.history.find()]
    return json_util.dumps({'history': reqs})