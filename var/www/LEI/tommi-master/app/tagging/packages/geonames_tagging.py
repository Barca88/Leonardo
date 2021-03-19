#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from os.path import join, dirname, realpath, exists
import nltk
import subprocess
from subprocess import PIPE
import json
from app import mongo

def readFile(file_path):
    f = open(file_path, "r")
    texto = f.read()
    return texto


def getWords(file_path):
    output = subprocess.run(['linguakit', 'tok', 'pt', file_path], encoding='utf-8', stdout=PIPE, stderr=PIPE)
    texto = output.stdout
    ner_classification = texto.split('\n')
    ner_classification = list(filter(None, ner_classification))
    words = []
    for s in ner_classification:
        tmp = {}
        tmp['word'] = s.split(' ')[0]
        tmp['position'] = len(words)
        tmp['anotated'] = False
        words.append(tmp)
    return words

def getLocais(locais_file_path):
    with open(locais_file_path, encoding='utf-8') as f:
        locais_data = json.load(f)
    #clean whitespaces and pontuation
    return locais_data

def getMaxLocalLength(locais_data):
    maximo = 0
    tamanho = len(locais_data)
    for local in locais_data:
        if tamanho > maximo:
            maximo = tamanho
    return maximo
    # for distrito in locais_data:
    #     tamanho = len(distrito["localidades"])
    #     for local in distrito["localidades"]:
    #         if tamanho > maximo:
    #             maximo = tamanho
    # return maximo


def createList(position, maximo, words):
    word_list = []
    inicio = 0
    while(inicio < maximo):
        if inicio == 0:
            word = words[position]['word']
            position = position + 1
            inicio = inicio + 1
            word_list.append(word)
        else:
            back = word_list[inicio-1]
            word = words[position]['word']
            word = back + " " + word
            word_list.append(word)
            position = position + 1
            inicio = inicio + 1
    return word_list

def checkWordLocal(word, locais_data):
    for local in locais_data:
        word_to_compare = local["nome"]
        if word == word_to_compare:
            return True        
    return False

def checkListLocal(position,word_list,locais_data):
    stop_pos = 0
    found = False
    for word in word_list:
        found = checkWordLocal(word,locais_data)
        if found == True:
            return found,stop_pos
        else:
            stop_pos = stop_pos + 1
    return found,stop_pos


def checkMaximo(posicao,maximo,tamanho):
    limite = int(tamanho) - int(posicao)
    if limite < (maximo):
        maximo = maximo - 1
    return maximo

def checkLocal(words,locais_data,maximo):
    verify = 0
    list_of_founds = []
    for word in words:
        position = word['position']
        if verify == position:
            maximo = checkMaximo(position,maximo,len(words))
            word_list = createList(position,maximo,words)
            found, stop_pos = checkListLocal(position,word_list,locais_data)
            if found == True:
                new = {}
                new['start'] = verify
                new['stop'] = verify + stop_pos
                list_of_founds.append(new)
                verify = verify + stop_pos + 1
            else:
                verify = verify +1
    return list_of_founds

def changeAnotation(words,list_of_founds):
    for found in list_of_founds:
        start = found['start']
        stop = found['stop']
        if start == stop:
            words[start]['anotated'] = True
        else:
            while(start < (stop +1)):
                words[start]['anotated'] = True
                start = start +1
    return words


def createTag(position,words):
    stop = False
    tag = "<local>" + words[position]['word']
    while(stop == False):
        position = position + 1
        if words[position]['anotated'] == False:
            tag = tag + "</local>"
            stop = True
        else:
            tag = tag + " " + words[position]['word']
    return tag,position


def writeText(words,anotated_path):
    f = open(anotated_path, "w")
    verify = 0
    for word in words:
        if word['position'] == verify:
            if word['anotated'] == False:
                f.write(word['word'])
                f.write(' ')
                verify = verify + 1
            else:
                tag,next_word = createTag(verify,words)
                f.write(tag)
                f.write(' ')
                verify = next_word
    f.close()
    text = readFile(anotated_path)
    return text


# if __name__ == "__main__":
#     file_path = './Folios/Folio196v.txt'
#     locais_path = './geonamesPTClean.json'
#     locais_data = getLocais(locais_path)
#     words = getWords(file_path)
#     maximo = getMaxLocalLength(locais_data)
#     list_of_founds = checkLocal(words,locais_data,5)
#     words = changeAnotation(words,list_of_founds)
#     writeText(words)

# Funções usadas para obter as coordenadas
def getCoordsPlace(place,locais_data):
    for local in locais_data:
        word_to_compare = local["nome"]
        if place == word_to_compare:
            newDict = {}
            newDict["nome"] = local["nome"]
            newDict["latitude"] = local["latitude"]
            newDict["longitude"] = local["longitude"]
            return newDict
    return None

def cleanResult(result):
    newResult = list()
    for r in result:
        if len(r["latitude"]) > 1:
            i = 0
            while i < len(r["latitude"]):
                new = dict()
                new["nome"] = r["nome"]
                new["latitude"] = float(r["latitude"][i])
                new["longitude"] = float(r["longitude"][i])
                newResult.append(new)
                i += 1
        else:
            new = dict()
            new["nome"] = r["nome"]
            new["latitude"] = float(r["latitude"][0])
            new["longitude"] = float(r["longitude"][0])
            newResult.append(new)
    return newResult

def insertPlaceMongo(place):
    localidade = mongo.db.localidades.find_one({"nome": place["nome"], "latitude": place["latitude"], "longitude": place["longitude"]})
    if localidade == None:
        mongo.db.localidades.insert_one(place)
    else:
        nFolios = place["nFolios"] + localidade["nFolios"]
        folios = []
        for folio in localidade["folios"]:
            folios.append(folio)
        for folio in place["folios"]:
            folios.append(folio)
        mongo.db.localidades.find_one_and_update({"_id": localidade["_id"]},{"$set":{"nFolios":nFolios, "folios": folios}})

def cleanPlaceAnotatedDb(place,name):
    folios = []
    folios.append(name)
    if len(place["latitude"]) > 0:
        i = 0
        while i < len(place["latitude"]):
            latest = mongo.db.localidades.find().sort('_id',-1).limit(1)
            latest = list(latest)
            if len(latest) > 0: 
                new = dict()
                new["_id"] = latest[0]["_id"] + 1
                new["nome"] = place["nome"]
                new["latitude"] = float(place["latitude"][i])
                new["longitude"] = float(place["longitude"][i])
                new["nFolios"] = 1
                new["remover"] = False
                new["folios"] = folios
                insertPlaceMongo(new)
            else:
                new = dict()
                new["_id"] = 1
                new["nome"] = place["nome"]
                new["latitude"] = float(place["latitude"][i])
                new["longitude"] = float(place["longitude"][i])
                new["nFolios"] = 1
                new["folios"] = folios
                new["remover"] = False
                insertPlaceMongo(new)
            i += 1
    else:
        latest = mongo.db.localidades.find().sort('_id',-1).limit(1)
        latest = list(latest)
        if len(latest) > 0:
            new = dict()
            new["_id"] = latest[0]["_id"] + 1
            new["nome"] = place["nome"]
            new["latitude"] = float(place["latitude"][0])
            new["longitude"] = float(place["longitude"][0])
            new["nFolios"] = 1
            new["folios"] = folios
            new["remover"] = False
            insertPlaceMongo(new)
        else:
            new = dict()
            new["_id"] = 1
            new["nome"] = place["nome"]
            new["latitude"] = float(place["latitude"][0])
            new["longitude"] = float(place["longitude"][0])
            new["nFolios"] = 1
            new["folios"] = folios
            new["remover"] = False
            insertPlaceMongo(new) 

def insertPlacesAnotated(text, locais_data,name):
    placesAnotated = re.findall(r'\<local\>(.+?)\<\/local\>',text)
    placesAnotated = list(dict.fromkeys(placesAnotated))
    for place in placesAnotated: 
        localidade = getCoordsPlace(place, locais_data)
        cleanPlaceAnotatedDb(localidade,name)


def tagging_file(file_path,placesList,name):
    newName = name.split('.')[0] + '_anotated.txt'
    anotated_path = join(dirname(realpath(__file__)), '..','georreferenciacao/static/doc/files_anotated', newName)
    if not exists(anotated_path):
        words = getWords(file_path)
        maximo = getMaxLocalLength(placesList)
        list_of_founds = checkLocal(words,placesList,5)
        words = changeAnotation(words,list_of_founds)
        text = writeText(words,anotated_path)
    else:
        text = 'Já Foram Processados os Ficheiros'
        words = 'Já Foram Processados os Ficheiros'
    return text,words