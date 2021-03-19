#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 16:34:44 2019

@author: Tommi
"""

#import mongoInit
import os
import datetime as dt
import re 
from app.indexador import extractor as extract 
import io


#index = mongoInit.getIndex()

#Função cuja funcionalidade é limpar o texto, retirando '\n'
def cleanText(texto):
    texto = re.sub(r"\n","",texto)
    return texto

#Função cuja finalidade é associar as linhas de um dado fólio já processado ao respetivo fólio em questão
def transformIndex(file,lines_to_insert,dic):
    for key, value in lines_to_insert.items():
        x = dic.get(key,0)
        if(x == 0):
            dic[key] = {}
            dic[key][file] = value
        else:
            dic[key][file] = value
    return dic


#Caso uma palavra se encontre repetida numa determinada linha, remove outras ocorrencias dessa linha, nao 
#havendo repetições 

def removeDuplicates(dic):
    for key, value in dic.items():
        novo = []
        for i in value:
            if i not in novo:
                novo.append(i)
        dic[key] = novo
    return dic

#Função que regista na coleção 'indexacao' cada indice, atribuindo o seu id, nº de ocurrencias e as suas referencias
'''
def addMongo(ocur_count,dic):
    nova_entrada = {}
    for key,value in ocur_count.items():
        nova_entrada["_id"] = key
        nova_entrada["n_ocorrencias"] = value
        nova_entrada["ocorrencias"] = dic[key]
        lista = []
        for key,value in dic[key].items():
            lista.append(key)   
        nova_entrada["ref"] = lista
        index.insert_one(nova_entrada)
'''

#Função que itera todos os folios da pasta 'Processados' e trata cada palavra de cada cada fólio.
#Para tal, é iterada cada linha de um documento e posteriormente cada palavra. Para cada palavra, é indicado
#o id (a palavra em questão), as suas ocorrências (indicadas pelo documento e a devida linha onde se encontra) 
#e pela referência, que diz respeito aos folios onde está inserida a palavra
'''
def indexFiles(pathFiles):
    ocur_count = {}
    dic = {}
    for file in pathFiles:
        linha = 0
        name, ext = os.path.splitext(file)
        if(ext == ".txt"):
            file_path = "./../Processados/" + file
            file_open = io.open(file_path,"r",encoding="utf-8")
            lines_to_insert = {}
            
            for line in file_open.readlines():
                linha = linha + 1
                line = cleanText(line)
                for word in re.findall(r"\w+",line.lower()):
                    ocur_count[word] = ocur_count.get(word,0) + 1
                    lines_to_insert.setdefault(word, []).append(linha)
            lines_to_insert = removeDuplicates(lines_to_insert)
            dic = transformIndex(name,lines_to_insert,dic)
            new_path = "./../Indexados/" + file
            os.rename(file_path,new_path)        
    addMongo(ocur_count,dic)
'''

def transformDict(ocur_count,dic):
    nova_entrada = {}
    novo = []
    for key,value in ocur_count.items():
        nova_entrada["_id"] = key
        nova_entrada["n_ocorrencias"] = value
        nova_entrada["ocorrencias"] = dic[key]
        lista = []
        for key,value in dic[key].items():
            lista.append(key)   
        nova_entrada["ref"] = lista
        novo.append(dict(nova_entrada))
    return novo

def removeTags(texto):
    texto = re.sub(r'<nl>',r'\n',texto)
    texto = re.sub(r"<\/?\w+>", "",texto)
    return texto

def indexFile(file):
    ocur_count = {}
    dic = {}
    lista = []
    linha = 0
    caminho, ext = os.path.splitext(file)
    array = caminho.split("/")
    array = [str(array[x]) for x in range(len(array))]
    name = array[len(array)-1]
    if ext == ".txt":
        file_open = io.open(file,"r",encoding="utf-8")
        lines_to_insert = {}
        for line in file_open.readlines():
            linha = linha + 1
            line = removeTags(line)
            line = cleanText(line) 
            for word in re.findall(r"\w+",line.lower()):
                word = str(word)
                ocur_count[word] = ocur_count.get(word,0) + 1
                lines_to_insert.setdefault(word, []).append(linha)
                lines_to_insert = removeDuplicates(lines_to_insert)
                dic = transformIndex(name,lines_to_insert,dic)
        lista = transformDict(ocur_count,dic)
        return lista