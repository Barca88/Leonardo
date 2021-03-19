#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:45:33 2019

@author: Tommi
"""

#import mongoInit
import os
import datetime as dt
import re 
from collections import Counter
import io

#folios = mongoInit.getFolios()


#Função cuja funcionalidade é limpar o texto, retirando '\n'
def cleanText(texto):
    texto = re.sub(r"\n","",texto)
    return texto



def removeTags(texto):
    texto = re.sub(r'<nl>',r'\n',texto)
    texto = re.sub(r"<\/?\w+>", "",texto)
    return texto

#Função que guarda os folios na base de dados, na coleção 'folios', e retira os respetivos documentos 
#da pasta 'Fontes' e coloca-os na pasta 'Processados', depois de os inserir. Para cada fólio, é verificado 
#se cada documento tem extensão '.txt', de seguida é limpo o texto (cleanText()) e por fim é atribuido e inserido
#o seu nome, texto e a data 
'''
def guardarTexto(pathFiles):
    dic = {}
    for file in pathFiles:
        name, ext = os.path.splitext(file)
        if(ext == ".txt"):
            file_path = "./../Fontes/" + file
            file_open = io.open(file_path,"r",encoding="utf-8")
            texto = file_open.read()
            texto = cleanText(texto)
            dic["_id"] = name
            dic["texto"] = texto
            dic["data"] = dt.datetime.utcnow()
            folios.insert_one(dic)
            new_path = "./../Processados/" + file
            os.rename(file_path,new_path)
'''


def extraiTexto(file):
    name, ext = os.path.splitext(file)
    if ext == ".txt":
        file_open = io.open(file,"r",encoding="utf-8")
        texto = file_open.read()
        return texto

def extraiTextoSTags(file):
    name, ext = os.path.splitext(file)
    if ext == ".txt":
        file_open = io.open(file,"r",encoding="utf-8")
        texto = file_open.read()
        texto = removeTags(texto)
        return texto

def extTags(texto,name):
    dic = {}
    novo = []
    listaTags = re.findall(r'<(\w+)>',texto)
    temp = Counter(listaTags)
    for t in temp:
        listaN = []
        dic["tag"] = '<'+t+'>'
        dic["n_ocorrencias"] = temp[t]
        dic["ref"] = [name]
        expressao = '<'+t+'>'+'(.*?)'+'<\/'+t +'>'
        listaC = re.findall(expressao,texto,re.DOTALL | re.MULTILINE)
        for i,val in enumerate(listaC):
                val = re.sub(r"<nl>"," ",val)
                val = re.sub(r"\s+"," ",val)
                listaC[i] = val
        listaC = list(dict.fromkeys(listaC))
        dicC = {}
        dicC = {name:listaC}
        listaN.append(dict(dicC))
        dic["conteudoTag"] = listaN 
        novo.append(dict(dic))
    return novo
    
def extraiTags(file):
    lista = []
    caminho, ext = os.path.splitext(file)
    array = caminho.split("/")
    array = [str(array[x]) for x in range(len(array))]
    name = array[len(array)-1]
    if ext == ".txt":
        file_open = io.open(file,"r",encoding="utf-8")
        texto = file_open.read()
        lista = extTags(texto,name)
        return lista

def getInfo(file,tags,indices):
    dic = {}
    file_open = io.open(file,"r",encoding="utf-8")
    dic["n_folios"] = 1
    dic["n_linhas"] = len(file_open.readlines())
    dic["n_indices"] = 0
    for i in indices:
        dic["n_indices"] += i["n_ocorrencias"]
    dic["n_tags"] = 0 
    for t in tags:
        dic["n_tags"] += t["n_ocorrencias"]
    return dic

