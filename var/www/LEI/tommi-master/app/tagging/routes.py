#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.tagging import blueprint
from flask import request, url_for
from os import path, remove, listdir
from os.path import join, dirname, realpath
from app.tagging.packages import atualizaGrafia as atualiza
from app.tagging.packages import generateLocais as genLocais
from app.tagging.packages import extra
from app.tagging.packages import anota as anota
from werkzeug.utils import secure_filename
import json
from bson import json_util
import os 
from app import mongo, token_required
from flask_pymongo import PyMongo

from flask_cors import CORS, cross_origin
CORS(blueprint)

@blueprint.route('/')
def route_template():
    return "1"

@blueprint.route('/atualiza')
def route_template_atualiza():
    atualiza.execute()
    return "Sucesso a atualizar grafia"

@blueprint.route('/criaLocais')
def route_template_dicLocais():
    genLocais.execute()
    return "Sucesso a criar o dicionario de locais"


@blueprint.route('/submeterFolio',methods=['POST'])
def route_submeterFolio():
    static_dir = './app/tagging/static/upload/manual/'
    folio_data = request.json
    folio = folio_data['folio']
    tamanho = len(listdir(static_dir)) + 1
    filename = static_dir + "manual_" + str(tamanho) + ".txt"
    f = open(filename,"w+")
    f.write(folio)
    f.write('\n')
    f.close()
    texto = anota.execute(filename)
    filenameToRemove = str(os.getcwd()) + "/" + filename
    os.system('rm ' + filenameToRemove)
    resultado = {}
    resultado["texto"] = texto
    return json.dumps({"texto": texto},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/tagsAtivas')
def route_template_tagsAtivas():
    tags = {}
    tags_ativas, info_tags, list_tags = extra.getTagsAtivas()
    tags['tags'] = tags_ativas
    tags['info_tags'] = info_tags
    tags['list_tags'] = list_tags
    return json.dumps({"tags": tags_ativas,"info_tags":info_tags, "list_tags": list_tags},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/regras',methods=['GET'])
def routeGetRegras():
    regras = {}
    regras_list = extra.getRegrasAtualizacao()
    regras['regras'] = regras_list
    return json.dumps({"regras": regras_list},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/regras/adiciona',methods=['POST'])
def routeAdicionaRegra():
    data = request.json
    nova_regra = data["regra"]
    callback = mongo.db.regras.insert(nova_regra)
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/regras/remove',methods=['POST'])
def routeRemoveRegra():
    data = request.json
    regra_remover = data["regra"]
    callback = mongo.db.regras.remove(regra_remover)
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/infoTag/<tag>')
def route_template_infoTag(tag):
    response = {}
    tags = {}
    tags_ativas, info_tags, list_tags  = extra.getTagsAtivas()
    tags['tags'] = tags_ativas
    tags['info_tags'] = info_tags
    if(tag in tags_ativas):
        info_tag = info_tags[tag]
        response["info_tag"] = info_tag
    return json.dumps({"info_tag": info_tag},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/tags/adiciona',methods=['POST'])
def routeAdicionaTag():
    data = request.json
    nova_tag = data["nova_tag"]
    nova_tag["_id"] = nova_tag["tag"]
    callback = mongo.db.tagsSistema.insert(nova_tag)
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/tags/remove',methods=['POST'])
def routeRemoveTag():
    data = request.json
    tag_remover = data["tag"]
    callback = mongo.db.tagsSistema.remove(tag_remover)
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/tags/edit',methods=['POST'])
def routeEditTag():
    data = request.json
    tag_edit = data["tag"]
    tag_id = data["id"]
    callback = mongo.db.tagsSistema.update({"_id": tag_id}, {"$set":tag_edit})
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)



@blueprint.route('/folio/guardar',methods=['POST'])
def routeGuardaFolio():
    data = request.json
    idFolio = data["id"]
    words = data["words"]
    extra.atualizaDicionarios(words)
    extra.atualizaFolio(words, idFolio)
    folio = {}
    folio["_id"] = idFolio
    folio["words"] = words
    result = mongo.db.foliosAnotados.find({"_id": idFolio})
    value = list(result)
    if(len(value) == 0):
        callback = mongo.db.foliosAnotados.insert(folio)
    else:
        callback = mongo.db.foliosAnotados.update({"_id":idFolio},{"$set":{"words":words}})
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)



@blueprint.route('/folio/foliosAnotados',methods=['GET'])
def routeGetFoliosAnotados():
    data = mongo.db.foliosAnotados.find()
    foliosAnotados = list(data)
    listaFoliosAnotados = []
    for folio in foliosAnotados:
        listaFoliosAnotados.append(folio["_id"])
    return json.dumps({"listaFoliosAnotados": listaFoliosAnotados},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/folio/foliosAtualizados',methods=['GET'])
def routeGetFoliosAtualizados():
    data = mongo.db.foliosAtualizados.find()
    foliosAtualizados = list(data)
    listaFoliosAtualizados = []
    for folio in foliosAtualizados:
        listaFoliosAtualizados.append(folio["_id"])
    return json.dumps({"listaFoliosAtualizados": listaFoliosAtualizados},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/folio/foliosAnotados/<folioId>',methods=['GET'])
def routeGetFolioAnotado(folioId):
    data = mongo.db.foliosAnotados.find({"_id": folioId})
    data_list = list(data)
    words = data_list[0]["words"]
    return json.dumps({"textoAnotado": words},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/folio/foliosAtualizados/<folioId>',methods=['GET'])
def routeGetFolioAtualizado(folioId):
    data = mongo.db.foliosAtualizados.find({"_id": folioId})
    data_list = list(data)
    words = data_list[0]["textoAtualizado"]
    return json.dumps({"textoAtualizado": words},indent=4,default=json_util.default, ensure_ascii=False)



@blueprint.route('/atualizarFolio/<folioId>',methods=['GET'])
def routeAtualizaFolio(folioId):
    data = mongo.db.folios.find({"_id": folioId})
    data_list = list(data)
    folio = data_list[0]["textoSTags"]
    refresh_folio, replacer_list = atualiza.atualizaFolio(folio)
    return json.dumps({"texto": refresh_folio, "replacerList":replacer_list},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/folioAtualizado/guardar',methods=['POST'])
def routeGuardaFolioAtualizado():
    data = request.json
    idFolio = data["id"]
    texto = data["texto"]
    replacerList = data["replacerList"]
    folio = {}
    folio["_id"] = idFolio
    folio["textoAtualizado"] = texto
    folio["replacerList"] = replacerList
    result = mongo.db.foliosAtualizados.find({"_id": idFolio})
    value = list(result)
    if(len(value) == 0):
        callback = mongo.db.foliosAtualizados.insert(folio)
    else:
        callback = mongo.db.foliosAtualizados.update({"_id":idFolio},{"$set":{"textoAtualizado":texto ,"replacerList": replacerLis }})
    return json.dumps({"callback": callback},indent=4,default=json_util.default, ensure_ascii=False)


@blueprint.route('/anotaBase',methods=['GET'])
def route_anotaBase():
    folios = mongo.db.folios.find()
    sucesso = 0
    for folio_info in folios:
        # anota folio
        folio = folio_info["textoSTags"]
        static_dir = './app/tagging/static/upload/manual/'
        tamanho = len(listdir(static_dir)) + 1
        filename = static_dir + "manual_" + str(tamanho) + ".txt"
        f = open(filename,"w+")
        f.write(folio)
        f.write('\n')
        f.close()
        words = anota.execute(filename)
        filenameToRemove = str(os.getcwd()) + "/" + filename
        os.system('rm ' + filenameToRemove)

        #guarda folio anotado
        idFolio = folio_info["_id"]
        extra.atualizaDicionarios(words)
        extra.atualizaFolio(words, idFolio)
        folioAnotado = {}
        folioAnotado["_id"] = idFolio
        folioAnotado["words"] = words
        result = mongo.db.foliosAnotados.find({"_id": idFolio})
        value = list(result)
        if(len(value) == 0):
            callback = mongo.db.foliosAnotados.insert(folioAnotado)
        else:
            callback = mongo.db.foliosAnotados.update({"_id":idFolio},{"$set":{"words":words}})
        sucesso = sucesso + 1
    return json.dumps({"sucesso": sucesso},indent=4,default=json_util.default, ensure_ascii=False)





