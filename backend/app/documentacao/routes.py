#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.documentacao import blueprint
from flask import render_template, request, url_for, send_from_directory
from app import mongo, token_required, admin_required, photo_auth
from os import path, remove, listdir
from os.path import join, dirname, realpath

###### new imports
import datetime
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######


@blueprint.route('/docs', methods=['GET'])
@token_required
def route_docs():
    docs = [doc for doc in mongo.db.documentacao.find()]
    nome = request.args.get('nome')
    return json_util.dumps({'docs': docs, 'nome': nome})


@blueprint.route('/adicionar', methods=['POST'])
@admin_required
def route_adicionar():
    titulo = request.form.get('titulo')
    existe = mongo.db.documentacao.find_one({"_id":titulo})
    nome = request.args.get('nome')
    if existe:
        return json_util.dumps({'nome': nome,'message':'já existe'})
    else:
        desc = request.form.get('desc')
        autores = request.form.get('autores')
        data = request.form.get('data')
        tipo = request.form.get('tipo')
        if 'ficheiro' in request.files:
            ficheiro = request.files['ficheiro']
            if ficheiro.filename != '':
                ficheiro.filename = titulo
                upload_path2 = join(dirname(realpath(__file__)), 'static/ficheiro/')
                ficheiro.save(upload_path2 + ficheiro.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/ficheiro/', titulo + ".pdf") 
                upload_path2 = join(dirname(realpath(__file__)), 'static/ficheiro/', titulo + ".pdf")
                copyfile(src, upload_path2)
        value = mongo.db.documentacao.insert({"_id":titulo,"desc":desc,"autores":autores,"data":data,"tipo":tipo})
        return json_util.dumps({'nome': nome})


@blueprint.route('/apagar/<doc>')
@admin_required
def route_apagar(doc):
    value = mongo.db.documentacao.remove({"_id":doc})
    upload_path = join(dirname(realpath(__file__)), 'static/ficheiro/', doc)
    if path.exists(upload_path): 
        remove(upload_path)
    docs = mongo.db.documentacao.find()
    nome = request.args.get('nome')
    return json_util.dumps({'docs': docs, 'nome': nome})


@blueprint.route('/ficheiro/<doc>', methods=['GET'])
@token_required
def route_cur(doc):
    pathC = join(dirname(realpath(__file__)), 'static/ficheiro/')
    return send_from_directory(pathC,doc,mimetype='application/pdf')