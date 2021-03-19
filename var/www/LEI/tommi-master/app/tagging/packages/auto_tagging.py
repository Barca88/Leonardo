#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import subprocess
import json
from app.tagging.packages import extra

def getLocais(locais_file_path):
    with open(locais_file_path, encoding='utf-8') as f:
        locais_data = json.load(f)
    #clean whitespaces and pontuation
    return locais_data

def getMaxLocalLength(locais_data):
    maximo = 0
    for distrito in locais_data:
        for dist_key,dist_val in distrito.items():
            tamanho = len(dist_key)
            if tamanho > maximo:
                maximo = tamanho
            for concelho in dist_val: 
                for conc_key,freguesias in concelho.items():
                    tamanho = len(conc_key)
                    if tamanho > maximo:
                        maximo = tamanho
                    for freg in freguesias:
                        tamanho = len(freg)
                        if tamanho > maximo:
                            maximo = tamanho
    return maximo


def createList(position, maximo, words):
    word_list = []
    inicio = 0
    while((inicio < maximo) and (position < len(words))):
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
    for distrito in locais_data:
        for dist_key,dist_val in distrito.items():
            word_to_compare = dist_key
            if word == word_to_compare:
                return True
            for concelho in dist_val: 
                for conc_key,freguesias in concelho.items():
                    word_to_compare = conc_key
                    if word == word_to_compare:
                        return True
                    for freg in freguesias:
                        word_to_compare = freg
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


def checkWord(word, dicionario):
    for word_dic in dicionario:
        if(word_dic == word):
            return True
    return False


def checkList(position,word_list,dicionario):
    stop_pos = 0
    found = False
    for word in word_list:
        found = checkWord(word,dicionario)
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


def checkTag(words,dicionario,maximo,tag_under_check):
    verify = 0
    list_of_founds = []
    for word in words:
        position = word['position']
        if verify == position:
            maximo = checkMaximo(position,maximo,len(words))
            word_list = createList(position,maximo,words)
            if(tag_under_check == "localidade"):
                found, stop_pos = checkListLocal(position,word_list,dicionario)
            else:
                found, stop_pos = checkList(position,word_list,dicionario)
            if found == True:
                new = {}
                new['start'] = verify
                new['stop'] = verify + stop_pos
                list_of_founds.append(new)
                verify = verify + stop_pos + 1
            else:
                verify = verify +1
    return list_of_founds

