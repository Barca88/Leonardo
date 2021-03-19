#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.importacao import blueprint
from flask import render_template,request,flash,redirect,url_for
from flask_login import login_required
from app import mongo,dadosFolio,indexList,tags
from app.indexador import indexacao as index, extractor as extract
import datetime
import os
from os.path import join, dirname, realpath


@blueprint.route('/')
@login_required
def route_template():
    global dadosFolio
    dadosFolio.clear()
    global indexList 
    indexList = []
    nome = request.args.get('nome')
    return render_template('import1.html',nome=nome)

@blueprint.route('/passo1/',methods=['GET','POST'])
@login_required
def route_template_passo1():
    global dadosFolio
    if request.method == 'GET':
        if 'ficheiro' in dadosFolio.keys():
            path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"]) 
            os.remove(path)
        if 'foto' in dadosFolio.keys():
            path = join(dirname(realpath(__file__)), '..', 'folios/static/pics', dadosFolio["foto"])
            os.remove(path)
        nome = request.args.get('nome')
        return render_template('import1.html',folios=dadosFolio,nome=nome)
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
                        foto.save(upload_path + foto.filename)
                nome = request.args.get('nome')
                return redirect(url_for('import_blueprint.route_template_passo2',nome=nome))

@blueprint.route('/passo2/')
@login_required
def route_template_passo2():
    global dadosFolio
    textoTags = dadosFolio["textoTags"].split("\n")
    textoSTags = dadosFolio["textoSTags"].split("\n")
    nome = request.args.get('nome')
    return render_template('import2.html',textoTags= textoTags,textoSTags= textoSTags,nome=nome)

@blueprint.route('/passo3/')
@login_required
def route_template_passo3():
    global dadosFolio
    nome = request.args.get('nome')
    if 'foto' in dadosFolio.keys():
        return render_template('import3.html',foto= dadosFolio['foto'],nome=nome)
    else:
        return redirect(url_for('import_blueprint.route_template_passo4',nome=nome))

@blueprint.route('/passo4/')
@login_required
def route_template_passo4():
    global tags
    global dadosFolio 
    tags = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    tags = extract.extraiTags(path_ficheiro)
    nome = request.args.get('nome')
    if 'foto' in dadosFolio.keys():
        return render_template('import4.html',tags=tags,foto=1,nome=nome)
    else:
        return render_template('import4.html',tags=tags,nome=nome)

@blueprint.route('/passo5/',methods=['GET','POST'])
@login_required
def route_template_passo5():
    global indexList
    global dadosFolio
    indexList = []
    path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
    lista = index.indexFile(path_ficheiro)
    indexList = lista
    nome = request.args.get('nome')
    return render_template('import5.html',list=indexList,nome=nome)

@blueprint.route('/passo6/',methods=['GET','POST'])
@login_required
def route_template_passo6():
    global indexList
    global tags
    global dadosFolio
    nome = request.args.get('nome')
    if request.method == 'GET':
        temp = {}
        path_ficheiro = join(dirname(realpath(__file__)), '..', 'folios/static/doc', dadosFolio["ficheiro"])
        temp = extract.getInfo(path_ficheiro,tags,indexList)
        temp["idFolio"] = dadosFolio["idFolio"]
        temp["descricao"] = dadosFolio["descricao"]
        temp["tipo"] = dadosFolio["tipo"]
        return render_template('import6.html',info=temp,nome=nome)
    else:
        if request.method == 'POST':
            now = datetime.datetime.now()
            data = now.strftime("%Y-%m-%d %H:%M")
            if 'observacao' in dadosFolio.keys():
                mongo.db.folios.insert({"_id":dadosFolio["idFolio"],"descricao":dadosFolio["descricao"],"versao":dadosFolio['versao'],'sumario':dadosFolio['sumario'],"tipo":dadosFolio["tipo"],"observacao":dadosFolio["observacao"],"textoCTags":dadosFolio["textoTags"],"textoSTags":dadosFolio["textoSTags"],"data":data})
            else:
                mongo.db.folios.insert({"_id":dadosFolio["idFolio"],"descricao":dadosFolio["descricao"],"tipo":dadosFolio["tipo"],"versao":dadosFolio['versao'],'sumario':dadosFolio['sumario'],"textoCTags":dadosFolio["textoTags"],"textoSTags":dadosFolio["textoSTags"],"data":data})
            for l in indexList:
                indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
                if indice:
                    n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
                    ocorrencias = []
                    for i in indice["ocorrencias"]:
                        ocorrencias.append(i)
                    ocorrencias.append(l["ocorrencias"])
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


@blueprint.route('/cancela/',methods=['GET'])
@login_required
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
