#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.users import blueprint
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
UPLOAD_FOLDER = './static/pics/'


@blueprint.route('/users', methods=['GET'])
@admin_required
#@token_required
#@login_required
def route_users():
    #users = mongo.db.users.find()
    type = request.args.get('type')
    user = request.args.get('nome')
    domains = None
    if(type is None):
        users= [doc for doc in mongo.db.users.find()]
    else:
        if(type == "all"):
            users= [doc for doc in mongo.db.users.find()]
            if(user is not None):
                write_log(user, 'Utilizadores/Gestão', '', 'successfull')
        else:
            users = mongo.db.users.find({"type":type})
            if(type == "responsible"):
                users = mongo.db.users.find({"type":"Teacher"})
                domains = mongo.db.domains.find()
                if(user is not None):
                    write_log(user, 'InformaçãoBase/Responsáveis', '', 'successfull')
            if(type == "Teacher" and user is not None):
                write_log(user, 'InformaçãoBase/Professores', '', 'successfull')
            if(type == "Student" and user is not None):
                write_log(user, 'InformaçãoBase/Alunos', '', 'successfull')
    return json_util.dumps({'users': users, 'nome': user, 'domains' : domains})
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
    studentNumber = request.form.get('studentNumber')
    print("sN")
    print(studentNumber)
    existeU = mongo.db.users.find_one({"$or": [{"_id":username},{"studentNumber":studentNumber}]})
    existeP = mongo.db.requests.find_one({"$or": [{"_id":username},{"studentNumber":studentNumber}]})
    user = request.args.get('nome')
    type = request.args.get('type')
    if existeP:
        mongo.db.requests.remove({"$or": [{"_id":username},{"studentNumber":studentNumber}]})
        upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', username)
        upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', username)
        if path.exists(upload_path): 
            remove(upload_path)
        if path.exists(upload_path2): 
            remove(upload_path2)
    if existeU:
        if user:
            if(type == "all"): 
                write_log(user, 'Utilizadores/Gestão', 'Adicionar utilizadores', 'failed')
            if(type == "responsible"): 
                write_log(user, 'InformaçãoBase/Responsáveis', 'Adicionar utilizadores', 'failed')
            if(type == "Teacher"): 
                write_log(user, 'InformaçãoBase/Professores', 'Adicionar utilizadores', 'failed')
            if(type == "Student"): 
                write_log(user, 'InformaçãoBase/Alunos', 'Adicionar utilizadores', 'failed') 
        print('user ja existe')
        return json_util.dumps({'nome': user,'message':'já existe'})
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
        mongo.db.users.insert({"_id":username,"name":name,"email":email,"studentNumber":studentNumber, "password":encryptPass,"type":tipo,"university":universidade,"department":departamento,"date":data,"comments":obs, "user_level": '0'})
        mongo.db.users.find()
        if user:
            if(type == "all"): 
                write_log(user, 'Utilizadores/Gestão', 'Adicionar utilizadores', 'successfull')
            if(type == "responsible"): 
                write_log(user, 'InformaçãoBase/Responsáveis', 'Adicionar utilizadores', 'successfull')
            if(type == "Teacher"): 
                write_log(user, 'InformaçãoBase/Professores', 'Adicionar utilizadores', 'successfull')
            if(type == "Student"): 
                write_log(user, 'InformaçãoBase/Alunos', 'Adicionar utilizadores', 'successfull') 
        return json_util.dumps({'nome': user})


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
    userAdmin = request.args.get('nome')
    action = request.args.get('action')
    type = request.args.get('type')
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if(action == "perfil"):
        write_log(userAdmin, 'Consultar Perfil', '', 'successfull')
    if photo_auth (request, user) and path.exists(pathCheck) :
        if(type == "all"): 
            write_log(userAdmin, 'Utilizadores/Gestão', 'Ver fotografia', 'successfull')
        if(type == "responsible"): 
            write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Ver fotografia', 'successfull')
        if(type == "Teacher"): 
            write_log(userAdmin, 'InformaçãoBase/Professores', 'Ver fotografia', 'successfull')
        if(type == "Student"): 
            write_log(userAdmin, 'InformaçãoBase/Alunos', 'Ver fotografia', 'successfull')
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        if(type == "all"): 
            write_log(userAdmin, 'Utilizadores/Gestão', 'Ver fotografia', 'failed')
        if(type == "responsible"): 
            write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Ver fotografia', 'failed')
        if(type == "Teacher"): 
            write_log(userAdmin, 'InformaçãoBase/Professores', 'Ver fotografia', 'failed')
        if(type == "Student"): 
            write_log(userAdmin, 'InformaçãoBase/Alunos', 'Ver fotografia', 'failed')
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

@blueprint.route('/foto/atualizar/<user>', methods=['POST'])
@token_required
def route_foto_atualizar(user):
    userAdmin = request.args.get('nome')
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
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
    else:
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar Foto', 'failed')
        return send_from_directory(pathPhoto, user, mimetype='image/png')

    if photo_auth (request, user) and path.exists(pathCheck) :
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar Foto', 'successfull')
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar Foto', 'failed')
        return send_from_directory(pathPhoto, "default", mimetype='image/png')



##########################################
@blueprint.route('/curriculo/<user>', methods=['GET'])
@token_required
def route_cur(user):
    userAdmin = request.args.get('nome')
    action = request.args.get('action')
    type = request.args.get('type')
    pathPhoto = join(dirname(realpath(__file__)), 'static/curriculo/')
    pathC = join(pathPhoto, user)
    

    if photo_auth (request, user) and  path.exists(pathC):
        if(action == "perfil"):
            write_log(userAdmin, 'Consular Perfil', 'Ver o curriculo', 'successfull')
        if(type == "all"): 
            write_log(userAdmin, 'Utilizadores/Gestão', 'Ver o curriculo', 'successfull')
        if(type == "responsible"): 
            write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Ver o curriculo', 'successfull')
        if(type == "Teacher"): 
            write_log(userAdmin, 'InformaçãoBase/Professores', 'Ver o curriculo', 'successfull')
        if(type == "Student"): 
            write_log(userAdmin, 'InformaçãoBase/Alunos', 'Ver o curriculo', 'successfull') 
        return send_from_directory(pathPhoto, user,mimetype='application/pdf')
    else :
        if(action == "perfil"):
            write_log(userAdmin, 'Consular Perfil', 'Ver o curriculo', 'failed')
        if(type == "all"): 
            write_log(userAdmin, 'Utilizadores/Gestão', 'Ver o curriculo', 'failed')
        if(type == "responsible"): 
            write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Ver o curriculo', 'failed')
        if(type == "Teacher"): 
            write_log(userAdmin, 'InformaçãoBase/Professores', 'Ver o curriculo', 'failed')
        if(type == "Student"): 
            write_log(userAdmin, 'InformaçãoBase/Alunos', 'Ver o curriculo', 'failed') 
        return

@blueprint.route('/curriculo/atualizar/<user>', methods=['POST'])
@token_required
def route_cur_atualizar(user):
    userAdmin = request.args.get('nome')
    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
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
    else:
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar curriculo', 'failed')
        return send_from_directory(pathC, user, mimetype='application/pdf')

    if photo_auth (request, user) :
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar curriculo', 'successfull')
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else :
        write_log(userAdmin, 'Consultar Perfil', 'Atualizar curriculo', 'failed')
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')
##########################################


@blueprint.route('/import_registos', methods=['POST'])
@token_required
def route_import_registos():
    print('teste1')
    if 'registos' in request.files:
        print('teste2')
        registos = request.files['registos']
        upload_path = join(dirname(realpath(__file__)), 'static/registos/')
        print("Registos: ", registos.filename)
        print("up path", upload_path)
        if registos.filename != '':
            upload_path2 = join(dirname(realpath(__file__)), 'static/registos/')
            filename = upload_path2 + registos.filename
            registos.save(filename)

            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    print(row)
                    if line_count == 0:
                        line_count += 1
                        # if len(row) > 10:
                        #     return json_util.dumps({'message':"Error"})
                    else:
                        encryptPass = generate_password_hash("password")
                        print(row)
                        value = mongo.db.requests.insert({"_id":row[2],"name":row[0],"email":row[6],"password":encryptPass,"type":"Student","university":row[5],"department":"","date":row[8],"comments":""})
                        line_count += 1
        
            # the result is a Python dictionary:
    print("teste3")
    newUsers = request.form.get('newUsers')

    user = request.args.get('nome')
    success = True

    jsonLst = json.loads(newUsers)
    list = []
    for jsonUser in jsonLst:
        if(mongo.db.users.find_one({"_id":jsonUser["eMail"].split("@")[0]})):
            list.append(mongo.db.users.find_one({"_id":jsonUser["eMail"].split("@")[0]}))
            success = False
        else:
            mongo.db.users.insert({"_id": jsonUser["eMail"].split("@")[0],"name":jsonUser["Nome"],"studentNumber":jsonUser["Identificador"],"email":jsonUser["eMail"],"password":generate_password_hash("password"),"type":jsonUser["Tipo"],"university":jsonUser["Instituição"],"department":jsonUser["Curso"], "level":jsonUser["Nível"], "gender":jsonUser["Género", "user_level": '0'] })
            #mongo.db.users.insert({"_id": jsonUser["eMail"].split("@")[0],"nome":jsonUser["Nome"],"email":jsonUser["eMail"],"password":generate_password_hash("password"),"tipo":jsonUser["Tipo"],"universidade":jsonUser["Instituição"],"departamento":jsonUser["Curso"], "validade":jsonUser["Validade"], "nivel":jsonUser["Nível"], "genero":jsonUser["Género"] })
        
    if(success):
        write_log(user, 'Utilizadores/Importação', 'Importar Utilizadores', 'successfull')
        return json_util.dumps({'nome': user})
    else:
        write_log(user, 'Utilizadores/Importação', 'Importar Utilizadores', 'failed')
        return json_util.dumps({'nome': user,'message':'já existe', 'list' : list})
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
    mongo.db.users.remove({"_id":user})
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user)
    if path.exists(upload_path): 
        remove(upload_path)
    if path.exists(upload_path2): 
        remove(upload_path2)
    users = mongo.db.users.find()
    userAdmin = request.args.get('nome')
    type = request.args.get('type')

    if(type == "all"): 
        write_log(userAdmin, 'Utilizadores/Gestão', 'Eliminar User', 'successfull')
    if(type == "responsible"): 
        write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Eliminar User', 'successfull')
    if(type == "Teacher"): 
        write_log(userAdmin, 'InformaçãoBase/Professores', 'Eliminar User', 'successfull')
    if(type == "Student"): 
        write_log(userAdmin, 'InformaçãoBase/Alunos', 'Eliminar User', 'successfull') 
    return json_util.dumps({'users': users})

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
    studentNumber = request.form.get('studentNumber')
    obs = request.form.get('obs')
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
        mongo.db.users.update({"_id":username},{"name":nome,"email":email,"studentNumber": studentNumber, "password":password,"type":tipo,"university":universidade,"department":departamento,"comments":obs})
    else:
        mongo.db.users.update({"_id":username},{"$set":{"name":nome, "studentNumber": studentNumber,"email":email,"type":tipo,"university":universidade,"department":departamento,"comments":obs}})    
    users = mongo.db.users.find()
    userAdmin = request.args.get('nome')
    type = request.args.get('type')
    if(type == "all"): 
        write_log(userAdmin, 'Utilizadores/Gestão', 'Editar utilizadores', 'successfull')
    if(type == "responsible"): 
        write_log(userAdmin, 'InformaçãoBase/Responsáveis', 'Editar utilizadores', 'successfull')
    if(type == "Teacher"): 
        write_log(userAdmin, 'InformaçãoBase/Professores', 'Editar utilizadores', 'successfull')
    if(type == "Student"): 
        write_log(userAdmin, 'InformaçãoBase/Alunos', 'Editar utilizadores', 'successfull') 
    return json_util.dumps({'users': users})

###### PEDIDOS ######

@blueprint.route('/pedidos', methods=['GET'])
@admin_required
@token_required
#@login_required
def route_pedidos():
    pedidos= [doc for doc in mongo.db.requests.find()]
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Pedidos de Acesso', '', 'successfull')
    return json_util.dumps({'pedidos': pedidos, 'nome': user})

@blueprint.route('/pedidos/registar', methods=['POST'])
#@admin_required
#@login_required
def route_template_registar_pedido():
    print("/pedidos/registar")
    username = request.form.get('username')
    existeU = mongo.db.users.find_one({"_id":username})
    existeP = mongo.db.requests.find_one({"_id":username})
    user = request.args.get('nome')
    type = request.args.get('type')
    if existeU or existeP:
        return json_util.dumps({'nome': user,'message':'já existe'})
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        encryptPass = generate_password_hash(password)
        tipo = request.form.get('tipo')
        universidade = request.form.get('universidade')
        departamento = request.form.get('departamento')
        studentNumber = request.form.get('studentNumber')
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
        mongo.db.requests.insert({"_id":username,"name":name,"email":email,"studentNumber": studentNumber, "password":encryptPass,"type":tipo,"university":universidade,"department":departamento,"date":data,"comments":obs})
        mongo.db.requests.find()
        return json_util.dumps({'nome': user})


@blueprint.route('/pedidos/ver/<pedido>', methods=['GET'])
@admin_required
#@login_required
def route_template_ver_pedido(pedido):
    nome = request.args.get('nome')
    existe = mongo.db.requests.find_one({"_id":pedido})
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
    userAdmin = request.args.get('nome')
    pathPhoto = join(dirname(realpath(__file__)), 'static/picsPedidos/')
    pathCheck = join(pathPhoto, pedido)
    if photo_auth (request, pedido) and path.exists(pathCheck) :
        write_log(userAdmin, 'Utilizadores/Pedidos de Acesso', 'Ver fotografia', 'successfull')
        return send_from_directory(pathPhoto, pedido, mimetype='image/png')
    else :
        write_log(userAdmin, 'Utilizadores/Pedidos de Acesso', 'Ver fotografia', 'failed')
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

##########################################
@blueprint.route('/pedidos/curriculo/<pedido>', methods=['GET'])
@token_required
def route_cur_pedido(pedido):
    userAdmin = request.args.get('nome')
    pathC = join(dirname(realpath(__file__)), 'static/curriculoPedidos/')
    print (pathC)
    print (pedido)
    if photo_auth (request, pedido) : 
        write_log(userAdmin, 'Utilizadores/Pedidos de Acesso', 'Ver currículo', 'successfull')
        return send_from_directory(pathC, pedido,mimetype='application/pdf')
    else :
        write_log(userAdmin, 'Utilizadores/Pedidos de Acesso', 'Ver currículo', 'failed')
        return send_from_directory(pathC, "Rafiki",mimetype='application/pdf')
##########################################

@blueprint.route('/pedidos/apagar/<pedido>')
@admin_required
#@login_required
def route_template_apagar_pedido(pedido):
    mongo.db.requests.remove({"_id":pedido})
    upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', pedido)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', pedido)
    if path.exists(upload_path): 
        remove(upload_path)
    if path.exists(upload_path2): 
        remove(upload_path2)
    pedidos = mongo.db.requests.find()
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Pedidos de Acesso', 'Eliminar Pedido', 'successfull')
    return json_util.dumps({'pedidos': pedidos})

@blueprint.route('/pedidos/mover/<pedido>')
@admin_required
#@login_required
def route_template_mover_pedido(pedido):
    value1 = mongo.db.requests.find_one({"_id": pedido})
    value1['user_level'] = '0'
    mongo.db.users.insert(value1)
    mongo.db.requests.remove({"_id":pedido})
    upload_path = join(dirname(realpath(__file__)), 'static/picsPedidos/', pedido)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculoPedidos/', pedido)
    if path.exists(upload_path):
        new_path = join(dirname(realpath(__file__)), 'static/pics/', pedido)
        rename(upload_path, new_path)
    if path.exists(upload_path2):
        new_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', pedido)
        rename(upload_path2, new_path2)
    pedidos = mongo.db.requests.find()
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Pedidos de Acesso', 'Confirmar submissão de utilizador', 'successfull')
    return json_util.dumps({'pedidos': pedidos})



@blueprint.route('/active', methods=['GET'])
@token_required
def route_active():
    users= [doc for doc in mongo.db.activeUsers.find()]
    date = datetime.datetime.now()
    date = date - datetime.timedelta(minutes = 15)
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Atividade Corrente', '', 'successfull')
    ret=[]
    for u in users:
        if datetime.datetime.strptime(u['stamp'],'%Y-%m-%d %H:%M:%S.%f') > date :
            ret.append(u)
    return json_util.dumps({'users': ret})
    #return render_template('users.html',users=users,nome=nome)

@blueprint.route('/import', methods=['GET'])
@token_required
def route_import():
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Importação', '', 'successfull')
    return json_util.dumps({'users': user})

@blueprint.route('/history', methods=['GET'])
@token_required
def route_history():
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Historial de Acesso', '', 'successfull')
    reqs= [doc for doc in mongo.db.history.find()]
    return json_util.dumps({'reqs': reqs})

@blueprint.route('/historyCleanse', methods=['GET'])
@token_required
def route_historyCleanse():
    user = request.args.get('nome')
    mongo.db.history.drop()
    write_log(user, 'Utilizadores/Historial de Acesso', 'Limpar histórico', 'successfull')
    reqs= [doc for doc in mongo.db.history.find()]
    return json_util.dumps({'history': reqs})


@blueprint.route('/pageLogs', methods=['GET'])
@admin_required
def route_pageLogs():
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Logs', '', 'successfull')
    reqs= [doc for doc in mongo.db.pageLogs.find()]
    return json_util.dumps({'reqs': reqs})


@blueprint.route('/pageLogsCleanse', methods=['GET'])
@token_required
def route_pageLogsCleanse():
    mongo.db.pageLogs.drop()
    user = request.args.get('nome')
    write_log(user, 'Utilizadores/Logs', 'Limpar Logs', 'successfull')
    reqs= [doc for doc in mongo.db.pageLogs.find()]
    return json_util.dumps({'history': reqs})