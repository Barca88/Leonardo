#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.importacao import blueprint
from flask import render_template,request,flash,redirect,url_for, send_from_directory
from flask_login import login_required
from app import mongo,dadosFolio,indexList,tags, token_required, admin_required
from app.indexador import indexacao as index, extractor as extract
import datetime
import os
from os.path import join, dirname, realpath
###### este é meu
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######
UPLOAD_FOLDER = '../folios/static/pics/'

"""
@blueprint.route('/')
@token_required
#@login_required
def route_template():
    global dadosFolio
    dadosFolio.clear()
    global indexList
    indexList = []
    nome = request.args.get('nome')
    return render_template('import1.html',nome=nome)

@blueprint.route('/passo1/',methods=['GET','POST'])
#@token_required
#@login_required
def route_template_passo1():
    global dadosFolio
    if request.method == 'GET':
        if 'ficheiro' in dadosFolio.keys():
            path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
            os.remove(path)
        if 'foto' in dadosFolio.keys():
            path = join(dirname(realpath(__file__)), '..', 'folios/static/pics', dadosFolio["foto"]+'.png')
            os.remove(path)
        nome = request.args.get('nome')
        return json_util.dumps({'nome': nome})
    else:
        if request.method == 'POST':
            folio = mongo.db.folios.find_one({"_id": request.form.get('idFolio')})
            if folio:
                flash('Este id já existe')
                nome = request.args.get('nome')
                return redirect(url_for('import_blueprint.route_template_passo1',nome=nome))
            else:
                dadosFolio.clear()
                dadosFolio['idFolio'] = request.form.get('idFolio')
                dadosFolio['descricao'] = request.form.get('descricao')
                dadosFolio['versao'] = request.form.get('versao')
                dadosFolio['sumario'] = request.form.get('sumario')
                dadosFolio['tipo'] = request.form.get('tipo')
                obs = request.form.get('obs')
                if obs :
                    dadosFolio['observacao'] = obs
                if 'ficheiro' in request.files:
                    ficheiro = request.files['ficheiro']
                    if ficheiro.filename == '':
                        flash('Não submeteu nenhum Ficheiro')
                        nome = request.args.get('nome')
                        return redirect(url_for('import_blueprint.route_template_passo1',nome=nome))
                    else:
                        ficheiro.filename = dadosFolio['idFolio'] + '.txt'
                        dadosFolio['ficheiro'] =  ficheiro.filename
                        path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', ficheiro.filename)
                        ficheiro.save(path)
                        path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
                        dadosFolio["textoTags"] = extract.extraiTexto(path_ficheiro)
                        dadosFolio["textoSTags"] = extract.extraiTextoSTags(path_ficheiro)
                if 'foto' in request.files:
                    foto = request.files['foto']
                    if foto.filename != '':
                        foto.filename = dadosFolio['idFolio']
                        dadosFolio['foto'] = foto.filename
                        upload_path = join(dirname(realpath(__file__)),'..' ,'folios/static/pics/')
                        foto.save(upload_path + foto.filename + '.png')
                nome = request.args.get('nome')
                return json_util.dumps({'nome': nome})
"""


@blueprint.route('/passo1/',methods=['POST'])
@admin_required
#@login_required
def route_template_passo1():
    if request.method == 'POST':
        folio = mongo.db.folios.find_one({"_id": request.form.get('idFolio')})
        nome = request.args.get('nome')
        if folio:
            flash('Este id já existe')
            return json_util.dumps({'nome': nome,'message':'O ID do Fólio já existe.'})
        else:
            if 'ficheiro' in request.files:
                ficheiro = request.files['ficheiro']
                if ficheiro.filename == '':
                    return json_util.dumps({'nome': nome,'message':'O Fólio não possui ficheiro.'})
                else:
                    ficheiro.filename = request.form.get('idFolio') + '.txt'
                    path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', ficheiro.filename)
                    ficheiro.save(path)
                    tags = []
                    indexList = []
                    tags = extract.extraiTags(path)
                    indexList = index.indexFile(path)
                    textoTags = extract.extraiTexto(path)
                    textoSTags = extract.extraiTextoSTags(path)
                    temp = extract.getInfo(path,tags,indexList)
                    os.remove(path)
                    return json_util.dumps({'nome': nome,'message':'não existe','textoTags':textoTags,'textoSTags':textoSTags,'tags':tags,'list':indexList,'passo6':temp})

"""
@blueprint.route('/passo2/')
#@token_required
#@login_required
def route_template_passo2():
    global dadosFolio
    textoTags = dadosFolio["textoTags"].split("\n")
    textoSTags = dadosFolio["textoSTags"].split("\n")
    nome = request.args.get('nome')
    return json_util.dumps({'textoTags':textoTags,'textoSTags':textoSTags,'nome': nome})
"""
"""
@blueprint.route('/passo3/', methods=['GET'])
#@token_required
#@login_required
def route_template_passo3():
    global dadosFolio
    nome = request.args.get('nome')
    if 'foto' in dadosFolio.keys():
        pathPhoto = join(dirname(realpath(__file__)),'..' ,'folios/static/pics/')
        folio = dadosFolio['idFolio'] + '.png'
        print (pathPhoto)
        print (folio)
        return send_from_directory(pathPhoto, folio, mimetype='image/png')
    else:
        print("file not found")
        return redirect(url_for('import_blueprint.route_template_passo4',nome=nome))


@blueprint.route('/passo4/')
#@token_required
#@login_required
def route_template_passo4():
    global tags
    global dadosFolio
    tags = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    tags = extract.extraiTags(path_ficheiro)
    nome = request.args.get('nome')
    if 'foto' in dadosFolio.keys():
        return json_util.dumps({'tags':tags,'foto':1,'nome': nome})
    else:
        return json_util.dumps({'tags':tags,'nome': nome})


@blueprint.route('/passo5/',methods=['GET','POST'])
#@token_required
#@login_required
def route_template_passo5():
    global indexList
    global dadosFolio
    indexList = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    lista = index.indexFile(path_ficheiro)
    indexList = lista
    nome = request.args.get('nome')
    return json_util.dumps({'list':indexList,'nome': nome})
"""
@blueprint.route('/passo6/',methods=['POST'])
@admin_required
#@login_required
def route_template_passo6():
    nome = request.args.get('nome')
    # if request.method == 'GET':
    #     print(request.form.get('tags'))
    #     print(request.form.get('indexList'))
    #     print(request.files['ficheiro'])
    #     temp = {}
    #     path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', request.files['ficheiro'].filename)
    #     tags = request.form.get('tags')
    #     indexList = request.form.get('indexList')
    #     temp = extract.getInfo(path_ficheiro,tags,indexList)
    #     # temp["idFolio"] = dadosFolio["idFolio"]
    #     # temp["descricao"] = dadosFolio["descricao"]
    #     # temp["tipo"] = dadosFolio["tipo"]         
    #     return json_util.dumps({'nome': nome, 'info':temp})
    # else:
    if 'ficheiro' in request.files:
        ficheiro = request.files['ficheiro']
        if ficheiro.filename == '':
            flash('Não submeteu nenhum Ficheiro')
            return json_util.dumps({'nome': nome, 'message':'nao correu bem'})
        else:
            ficheiro.filename = request.form.get('idFolio') + '.txt'
            path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', ficheiro.filename)
            ficheiro.save(path)
            tags = []
            indexList = []
            tags = extract.extraiTags(path)
            indexList = index.indexFile(path)
    if 'foto' in request.files:
        foto = request.files['foto']
        if foto.filename != '':
            foto.filename = request.form.get('idFolio')
            upload_path = join(dirname(realpath(__file__)),'..' ,'folios/static/pics/')
            foto.save(upload_path + foto.filename + '.png')
    now = datetime.datetime.now()
    data = now.strftime("%Y-%m-%d %H:%M")
    if 'observacao' in dadosFolio.keys():
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"tipo":request.form.get('tipo'),"observacao":request.form.get('obs'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data,"user":request.args.get('nome')})
    else:
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"tipo":request.form.get('tipo'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data,"user":request.args.get('nome')})
    for l in indexList:
        indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
        if indice:
            n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
            ocorrencias = []
            for i in indice["ocorrencias"]:
                ocorrencias.append(i)
            for i in l["ocorrencias"]:
                newDict = {}
                newDict[i] = l["ocorrencias"][i]
                ocorrencias.append(newDict)
            ref = []
            for i in indice["ref"]:
                ref.append(i)
            for i in l["ref"]:
                ref.append(i)
            mongo.db.indexacao.find_one_and_update({"_id": l["_id"]},{"$set": {"n_ocorrencias":n_ocorrencias,"ocorrencias":ocorrencias,"ref":ref}})
        else:
            ocorrencias = []
            ocorrencias.append(l["ocorrencias"])
            mongo.db.indexacao.insert_one({"_id":l["_id"],"n_ocorrencias":l["n_ocorrencias"],"ocorrencias":ocorrencias,"ref":l["ref"]})
    n_ocorrencias = 0
    for t in tags:
        tag = mongo.db.tags.find_one({"_id":t["tag"]})
        if tag:
            n_ocorrencias = tag["n_ocorrencias"]+t["n_ocorrencias"]
            ref = []
            for i in tag["ref"]:
                ref.append(i)
            for i in t["ref"]:
                ref.append(i)
            conteudo = []
            for i in tag["conteudoTag"]:
                conteudo.append(i)
            for i in t["conteudoTag"]:
                conteudo.append(i)
            mongo.db.tags.find_one_and_update({"_id": t["tag"]},{"$set":{"n_ocorrencias":n_ocorrencias,"ref":ref,"conteudoTag":conteudo}})
        else:
            mongo.db.tags.insert_one({"_id":t["tag"],"n_ocorrencias":t["n_ocorrencias"],"ref":t["ref"],"conteudoTag":t["conteudoTag"]})
    
    return json_util.dumps({'nome': nome, 'message':'inserido com sucesso'})
"""
@blueprint.route('/cancela/',methods=['GET'])
#@token_required
#@login_required
def route_template_cancela():
    global dadosFolio
    if 'ficheiro' in dadosFolio.keys():
        path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
        os.remove(path)
    if 'foto' in dadosFolio.keys():
        path = join(dirname(realpath(__file__)), '..', 'folios/static/pics', dadosFolio["foto"])
        os.remove(path)
    nome = request.args.get('nome')
    return redirect(url_for('home_blueprint.index',nome=nome))


@blueprint.route('/skip/',methods=['POST'])
#@token_required
#@login_required
def route_template_skip():
    global tags
    global dadosFolio
    global indexList
    tags = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    tags = extract.extraiTags(path_ficheiro)
    indexList = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    lista = index.indexFile(path_ficheiro)
    indexList = lista
    nome = request.args.get('nome')
    now = datetime.datetime.now()
    data = now.strftime("%Y-%m-%d %H:%M")
    if 'observacao' in dadosFolio.keys():
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"tipo":request.form.get('tipo'),"observacao":request.form.get('obs'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data})
    else:
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"tipo":request.form.get('tipo'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data})
    for l in indexList:
        indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
        if indice:
            n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
            ocorrencias = []
            for i in indice["ocorrencias"]:
                ocorrencias.append(i)
            for i in l["ocorrencias"]:
                newDict = {}
                newDict[i] = l["ocorrencias"][i]
                ocorrencias.append(newDict)
            ref = []
            for i in indice["ref"]:
                ref.append(i)
            for i in l["ref"]:
                ref.append(i)
            mongo.db.indexacao.find_one_and_update({"_id": l["_id"]},{"$set": {"n_ocorrencias":n_ocorrencias,"ocorrencias":ocorrencias,"ref":ref}})
        else:
            ocorrencias = []
            ocorrencias.append(l["ocorrencias"])
            mongo.db.indexacao.insert_one({"_id":l["_id"],"n_ocorrencias":l["n_ocorrencias"],"ocorrencias":ocorrencias,"ref":l["ref"]})
    n_ocorrencias = 0
    for t in tags:
        tag = mongo.db.tags.find_one({"_id":t["tag"]})
        if tag:
            n_ocorrencias = tag["n_ocorrencias"]+t["n_ocorrencias"]
            ref = []
            for i in tag["ref"]:
                ref.append(i)
            for i in t["ref"]:
                ref.append(i)
            conteudo = []
            for i in tag["conteudoTag"]:
                conteudo.append(i)
            for i in t["conteudoTag"]:
                conteudo.append(i)
            mongo.db.tags.find_one_and_update({"_id": t["tag"]},{"$set":{"n_ocorrencias":n_ocorrencias,"ref":ref,"conteudoTag":conteudo}})
        else:
            mongo.db.tags.insert_one({"_id":t["tag"],"n_ocorrencias":t["n_ocorrencias"],"ref":t["ref"],"conteudoTag":t["conteudoTag"]})
    return redirect(url_for('folios_blueprint.route_template_folios',nome=nome))
"""

@blueprint.route('/reindex/',methods=['GET'])
@admin_required
#@login_required
def route_template_reindex():
    mongo.db.indexacao.drop()
    textos = [doc for doc in mongo.db.folios.find({},{'textoSTags':1})] 
    for texto in textos:
        lista = []
        lista = index.indexDB(texto['textoSTags'],texto['_id'])
        for l in lista:
            indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
            if indice:
                n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
                ocorrencias = []
                for i in indice["ocorrencias"]:
                    ocorrencias.append(i)
                for i in l["ocorrencias"]:
                    newDict = {}
                    newDict[i] = l["ocorrencias"][i]
                    ocorrencias.append(newDict)
                ref = []
                for i in indice["ref"]:
                    ref.append(i)
                for i in l["ref"]:
                    ref.append(i)
                mongo.db.indexacao.find_one_and_update({"_id": l["_id"]},{"$set": {"n_ocorrencias":n_ocorrencias,"ocorrencias":ocorrencias,"ref":ref}})
            else:
                ocorrencias = []
                ocorrencias.append(l["ocorrencias"])
                mongo.db.indexacao.insert_one({"_id":l["_id"],"n_ocorrencias":l["n_ocorrencias"],"ocorrencias":ocorrencias,"ref":l["ref"]})
    return json_util.dumps({'message':'ok'})
