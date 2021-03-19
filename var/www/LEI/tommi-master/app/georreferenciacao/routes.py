#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from app.base import blueprint
from app import mongo, token_required
import re
import json
from app.tagging.packages import geonames_tagging as tagging
from bson import json_util 
from os.path import join, dirname, realpath
import os

from flask_cors import CORS, cross_origin
CORS(blueprint)

@blueprint.route('/getPlaces')
@token_required
def route_geo_places():
    result = mongo.db.localidades.find({"remover": False})
    return json.dumps(list(result),indent=4,default=json_util.default, ensure_ascii=False)
    


@blueprint.route('/process')
@token_required
def route_processa():
    placesList = mongo.db.places.find()
    placesList = list(placesList)
    dir_path = join(dirname(realpath(__file__)), '..','folios/static/doc')
    for root, dirs,files in os.walk(dir_path,topdown = False):
        for name in files:
            file_path = join(root, name)
            text,words = tagging.tagging_file(file_path,placesList,name)
            if text != 'Já Foram Processados os Ficheiros':
                tagging.insertPlacesAnotated(text,placesList,name)      
    # folio_filename = 'Folio196v.txt'
    # file_path = join(dirname(realpath(__file__)), 'static/doc/', folio_filename)
    # text,words = tagging.tagging_file(file_path,placesList)
    # tagging.insertPlacesAnotated(text,placesList)
    return json.dumps({message: 'Já Foram Processados os Ficheiros'},indent=4,default=json_util.default, ensure_ascii=False)

@blueprint.route('/remove',methods=['POST'])
@token_required
def route_remove_localidade():
    data = request.json
    mongo.db.localidades.find_one_and_update({"nome": data["nome"],"latitude": data["latitude"], "longitude": data["longitude"] },{"$set":{"remover":True}})
    return 'Elemento removido com sucesso'
