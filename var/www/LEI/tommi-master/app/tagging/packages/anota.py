#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import subprocess
import json
from app.tagging.packages import extra
from app.tagging.packages import man_tagging as man
from app.tagging.packages import auto_tagging as auto
from app.tagging.packages import atualizaGrafia as atualiza
from subprocess import PIPE

def getWords(file_path):
    output = subprocess.run(['linguakit', 'tagger', 'pt', file_path], encoding='utf-8',stdout=PIPE, stderr=PIPE)
    texto = output.stdout
    ner_classification = texto.split('\n')
    ner_classification = list(filter(None, ner_classification))
    words = []
    for s in ner_classification:
        if(s.split(' ')[0] != "<blank>"):
            tmp = {}
            tmp['word'] = s.split(' ')[0]
            tmp['normalization'] = s.split(' ')[1]
            aux_class = s.split(' ')[2]
            if len(aux_class)>2:
                tmp['classification'] = str(aux_class[0]) + str(aux_class[1])
            else:
                tmp['classification'] = aux_class
            tmp['position'] = len(words)
            tmp['ignoreCase'] = tmp['word'].lower()
            tmp['anotated'] = False
            tmp['tipo'] = ""
            tmp['color'] = "black"
            words.append(tmp) 
    return words


def createTag(position,words, tag_name):
    stop = False
    tamanho = len(words)
    tag = "<" + tag_name + "> " + words[position]['word']
    s_tag = words[position]['word'] 
    while(stop == False):
        position = position + 1
        if(position != tamanho):
            if words[position]['anotated'] == False:
                tag = tag + " </" + tag_name + ">"
                stop = True
            else:
                tag = tag + " " + words[position]['word']
                s_tag = s_tag + " " + words[position]['word']
        else:
            tag = tag + " </" + tag_name + ">"
            stop = True      
    return tag,s_tag,position

def sendText(words):
    texto_tags = []
    verify = 0
    for word in words:
        if word['position'] == verify:
            if word['anotated'] == False:
                tmp = {}
                tmp['word'] = word['word']
                tmp['s_tag'] = word['word']
                tmp['position'] = len(texto_tags)
                tmp['anotated'] = word['anotated']
                tmp['tipo'] = word['tipo']
                tmp['color'] = word['color']
                tmp['selected'] = False
                texto_tags.append(tmp)
                verify = verify + 1
            else:
                tag_tipo = word["tipo"]
                tag_color = word["color"]
                tmp = {}
                tag,s_tag,next_word = createTag(verify,words,tag_tipo)
                tmp['word'] = tag
                tmp['s_tag'] = s_tag
                tmp['position'] = len(texto_tags)
                tmp['anotated'] = True
                tmp['tipo'] = tag_tipo
                tmp['color'] = tag_color
                tmp['selected'] = False 
                texto_tags.append(tmp)
                verify = next_word
    return texto_tags

def changeAnotation(words,list_of_founds,tag_name,tag_color):
    tamanho = len(words)
    for found in list_of_founds:
        start = found['start']
        stop = found['stop']
        if start == stop:
            words[start]['anotated'] = True
            words[start]['tipo'] = tag_name
            words[start]['color'] = tag_color 
        else:
            while(start < (stop +1)):
                if(start != tamanho):
                    words[start]['anotated'] = True
                    words[start]['tipo'] = tag_name
                    words[start]['color'] = tag_color
                start = start +1
    return words


def formataWords(words):
    tamanho = len(words)
    i = 0
    for word in words:
        if(word['normalization'] == 'de'):
            nextIndex = i + 1
            if(nextIndex != tamanho):
                nextWord = words[nextIndex]
                if(nextWord['normalization'] == 'o'):
                    words.remove(nextWord)
                    tamanho = len(words)
                    word['word'] = 'do'
                    word['ignoreCase'] = 'do'
                    word['normalization'] = 'de o'
                if(nextWord['normalization'] == 'a'):
                    words.remove(nextWord)
                    tamanho = len(words)
                    word['word'] = 'da'
                    word['ignoreCase'] = 'da'
                    word['normalization'] = 'de a'
        if(word['normalization'] == 'a'):
            nextIndex = i + 1
            if(nextIndex != tamanho):
                nextWord = words[nextIndex]
                if(nextWord['normalization'] == 'a'):
                    words.remove(nextWord)
                    tamanho = len(words)
                    word['word'] = 'à'
                    word['ignoreCase'] = 'à'
                    word['normalization'] = 'a a'
                if(nextWord['normalization'] == 'o'):
                    words.remove(nextWord)
                    tamanho = len(words)
                    word['word'] = 'ao'
                    word['ignoreCase'] = 'ao'
                    word['normalization'] = 'a o'
        i = i + 1
    words = formatPositions(words)
    return words

def formatPositions(words):
    i = 0
    for word in words:
        word['position'] = i
        i = i + 1
    return words


def executeManual(folio):
    tags_ativas , tags_ativas_info, list_tags = extra.getTagsAtivas()
    words = getWords(folio)
    stop_words = getClassificationList(words)
    for tag in tags_ativas:
        info_tag = tags_ativas_info[tag]
        tag_color = info_tag["cor"]
        start_words = info_tag["start"]
        if(len(start_words) > 0 and len(stop_words) > 0):
            potencial_words = man.getPotentialWords(start_words,words, stop_words)
            words = changeAnotation(words,potencial_words, tag, tag_color)
    texto = sendText(words)
    return texto


def executeAuto(folio):
    tags_ativas , tags_ativas_info, list_tags = extra.getTagsAtivas()
    words = getWords(folio)
    for tag in tags_ativas:
        info_tag = tags_ativas_info[tag]
        tag_color = info_tag["cor"]
        dicionario_tag = info_tag["dicionario"]
        if(len(dicionario_tag) > 0):
            #maximo = getMaxLocalLength(tags_ativas_data)
            list_of_founds = auto.checkTag(words,dicionario_tag,5,tag)
            words = changeAnotation(words,list_of_founds,tag,tag_color)
    texto = sendText(words)
    return texto


def execute(folio):
    tags_ativas , tags_ativas_info, list_tags = extra.getTagsAtivas()
    words = getWords(folio)
    words = formataWords(words)
    stop_words = man.getClassificationList(words)
    for tag in tags_ativas:
        info_tag = tags_ativas_info[tag]
        tag_color = info_tag["cor"]
        start_words = info_tag["start"]
        dicionario_tag = info_tag["dicionario"]
        #auto
        if(len(dicionario_tag) > 0):
            #maximo = getMaxLocalLength(tags_ativas_data)
            list_of_founds = auto.checkTag(words,dicionario_tag,5,tag)
            words = changeAnotation(words,list_of_founds,tag,tag_color)
        #manual
        if(len(start_words) > 0 and len(stop_words) > 0):
            potencial_words = man.getPotentialWords(start_words,words, stop_words)
            words = changeAnotation(words,potencial_words, tag, tag_color)
            if(tag == 'nome'):
                potencial_names = man.getNomesProprios(words)
                words = changeAnotation(words, potencial_names, tag, tag_color)
    texto = sendText(words)
    return texto


