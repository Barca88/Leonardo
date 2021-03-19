#!/usr/bin/python3
# -*- coding: utf-8 -*-
from app import mongo, token_required
from flask_pymongo import PyMongo
import re
import os
import subprocess
import json

tags_path = './app/tagging/packages/static/json/tags_ativas.json'
regras_path = './app/tagging/packages/static/json/regras_atualizagrafia.json'

def readFile(file_path):
    f = open(file_path, "r")
    texto = f.read()
    return texto


def getTagsAtivas():
    tags_ativas = []
    list_tags = []
    info_tags = {}
    data = mongo.db.tagsSistema.find()
    tags = list(data)
    for tag in tags:
        tags_ativas.append(tag['tag'])
        info_tags[tag['tag']]= tag
        list_tags.append(tag)
    return tags_ativas, info_tags, list_tags


def getRegrasAtualizacao():
    data = mongo.db.regras.find()
    regras = list(data)
    return regras


def getIndicadoresStop():
    indicadoresStop = []
    indicadoresStop_path = './app/tagging/packages/static/json/indicadoresStop_classe.json'
    with open(indicadoresStop_path, encoding='utf-8') as f:
        indicadoresStop = json.load(f)
    return indicadoresStop



def atualizaDicionarios(words):
    indicadoresStop = []
    tags_ativas, info_tags, list_tags = getTagsAtivas()
    for word in words:
        if(word['tipo'] != "" and word['tipo'] != "localidade"):
            tag = word['tipo']
            entrada = word['s_tag']
            dicionario = info_tags[tag]["dicionario"]
            if(entrada not in dicionario):
                dicionario.append(entrada)
                mongo.db.tagsSistema.update({"_id":tag}, {"$set":{"dicionario":dicionario}})


def atualizaFolio(folio, idFolio):
    texto = ""
    for word in folio:
        texto = texto + word['word']
        texto = texto + " "
    mongo.db.folios.update({"_id":idFolio}, {"$set":{"textoCTags":texto}})
