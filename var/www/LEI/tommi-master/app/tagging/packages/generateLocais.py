#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from itertools import groupby
from operator import itemgetter
import re
import json


main_file = './app/tagging/packages/static/csv/freguesias-metadata.csv'
file1 = './app/tagging/packages/static/json/locais.json'
file2 = './app/tagging/packages/static/json/locaisLimpos.json'


def cleanWord(word):
    word = word.lower()
    word = re.sub(r'á',r'a',word)
    word = re.sub(r'à',r'a',word)
    word = re.sub(r'ã',r'a',word)
    word = re.sub(r'â',r'a',word)
    word = re.sub(r'é',r'e',word)
    word = re.sub(r'ẽ',r'e',word)
    word = re.sub(r'ê',r'e',word)
    word = re.sub(r'í',r'i',word)
    word = re.sub(r'ó',r'o',word)
    word = re.sub(r'õ',r'o',word)
    word = re.sub(r'ô',r'o',word) 
    word = re.sub(r'ú',r'u',word)
    return word

def cleanFreg(listaFreg):
    newList = []
    for freg in listaFreg:
        freguesia = cleanWord(freg)
        newList.append(freguesia)
    return newList

def removeAccentuation(locais):
    newList = []
    newList = locais.copy()
    for distrito in newList:
        for d in distrito:
            d1 = cleanWord(d)
            distrito[d1] = distrito.pop(d)
            for c in distrito[d1]:
                for concelho in c:
                    concelho2 = cleanWord(concelho)
                    c[concelho2] = c.pop(concelho)
                    c[concelho2] = cleanFreg(c[concelho2])
    return newList
                    

def createFreguesias(items):
    listaFreg = []
    for i in items:
        freguesia = i['freguesia']
        freguesia = re.sub(r'União das freguesias d[e|o|a] ','',freguesia)
        freguesia = re.sub(r'\(',',',freguesia)
        freguesia = re.sub(r'\)','',freguesia)
        if re.match(r'.+ e .+',freguesia):
            freguesia = re.sub(r' e ',';',freguesia)
            freguesias = freguesia.split(';')
            j = 0
            while j < len(freguesias):
                freguesia3 = freguesias[j]
                if ',' in freguesias[j]:
                    freguesias2 = freguesias[j].split(',')
                    k = 0
                    while k < len(freguesias2):
                        freguesia3 = freguesias2[k]
                        if re.match(r'.+\/.+',freguesia3):
                            freguesias4 = freguesia3.split('/')
                            y=0
                            while y < len(freguesias4):
                                freguesia5 = freguesias4[y]
                                if re.match(r'.+ - .+',freguesia5):
                                    freguesias6 = freguesia5.split('-')
                                    z = 0
                                    while z < len(freguesias6):
                                        freguesia7 = freguesias6[z]
                                        freguesia7 = freguesia7.strip()
                                        listaFreg.append(freguesia7)
                                        z +=1
                                else:
                                    freguesia5 = freguesia5.strip()
                                    listaFreg.append(freguesia5)
                                y +=1
                        else:
                            if re.match(r'.+ - .+',freguesia3):
                                freguesias4 = freguesia3.split('-')
                                y = 0
                                while y < len(freguesias4):
                                    freguesia5 = freguesias4[y]
                                    freguesia5 = freguesia5.strip()
                                    listaFreg.append(freguesia5)
                                    y +=1
                            else:
                                freguesia3 = freguesia3.strip()
                                listaFreg.append(freguesia3)
                        k+=1      
                else:
                    if re.match(r'.+\/.+',freguesias[j]):
                        y = 0
                        freguesias4 = freguesia3.split('/')
                        while y<len(freguesias4):
                            freguesia5 = freguesias4[y]
                            if re.match(r'.+ - .+',freguesia5):
                                freguesias6 = freguesia5.split('-')
                                k = 0
                                while k < len(freguesias6):
                                    freguesia7 = freguesias6[k]
                                    freguesia7 = freguesia7.strip()
                                    listaFreg.append(freguesia7)
                                    k+=1
                            else:
                                freguesia5.strip()
                                listaFreg.append(freguesia5)
                            y+=1
                    else:
                        if re.match(r'.+ - .+',freguesia3):
                            freguesias4 = freguesia3.split('-')
                            y = 0
                            while y < len(freguesias4):
                                freguesia5 = freguesias4[y]
                                freguesia5 = freguesia5.strip()
                                listaFreg.append(freguesia5)
                                y +=1
                        else:
                            freguesia3.strip()
                            listaFreg.append(freguesia3)
                j+=1
        else:
            if ',' in freguesia:
                freguesias2 = freguesia.split(',')
                j = 0
                while j<len(freguesias2):
                    freguesia3 = freguesias2[j]
                    if re.match(r'.+\/.+',freguesia3):
                        k = 0
                        freguesias4 = freguesia3.split('-')
                        while k < len(freguesias4):
                            freguesia5 = freguesias4[k]
                            if re.match(r'.+ - .+',freguesia5):
                                y = 0
                                freguesias6 = freguesia5.split('-')
                                while y < len(freguesias6):
                                    freguesia7 = freguesias6[y]
                                    freguesia7 = freguesia7.strip()
                                    listaFreg.append(freguesia7)
                                    y += 1
                            else:
                                freguesia5 = freguesia5.strip()
                                listaFreg.append(freguesia5)
                            k += 1
                    else:
                        if re.match(r'.+ - .+',freguesia3):
                            freguesias4 = freguesia3.split('-')
                            k = 0
                            while k < len(freguesias4):
                                freguesia5 = freguesias4[k]
                                freguesia5 = freguesia5.strip()
                                listaFreg.append(freguesia5)
                                k += 1
                        else:
                            freguesia3 = freguesia3.strip()
                            listaFreg.append(freguesia3)
                    j += 1
            else:
                if re.match(r'.+\/.+',freguesia):
                    freguesias2 = freguesia.split('/')
                    j = 0
                    while j < len(freguesias2):
                        freguesia3 = freguesias2[j]
                        if re.match(r'.+ - .+',freguesia3):
                            freguesias4 = freguesia3.split('-')
                            k = 0
                            while k < len(freguesias4):
                                freguesia5 = freguesias4[k]
                                freguesia5 = freguesia5.strip()
                                listaFreg.append(freguesia5)
                                k += 1
                        else:
                            freguesia3 = freguesia3.strip()
                            listaFreg.append(freguesia3)
                        j += 1
                else:
                    if re.match(r'.+ - .+',freguesia):
                        print(freguesia)
                        freguesias2 = freguesia.split('-')
                        j = 0
                        while j < len(freguesias2):
                            freguesia3 = freguesias2[j]
                            freguesia3 = freguesia3.strip()
                            listaFreg.append(freguesia3)
                            j += 1
                    else:
                        freguesia = freguesia.strip()
                        listaFreg.append(freguesia)
    return listaFreg                  



def createPlaces(file):
    with open(file, 'r') as file:
        csv_file = csv.DictReader(file,delimiter=';')
        lista = []
        for row in csv_file:
            dicRow = dict(row)
            lista.append(dicRow)
        listaLocais = []
        listaDistritos = []
        listaConcelhos = []
        for key,items in groupby(lista,key=itemgetter('concelho')):
            listaFreg = []
            listaFreg = createFreguesias(items)
            concelhosDic = {}
            concelhosDic[key] = listaFreg
            listaConcelhos.append(concelhosDic)
        for key,items in groupby(lista,key=itemgetter('distrito')):
            listaCon = []
            for i in items:
                listaCon.append(i['concelho'])
            listaCon = list(dict.fromkeys(listaCon))
            listaCon2 = []
            for c in listaCon:
                new_dic = {}
                new_dic[c] = None
                listaCon2.append(new_dic)
            distritosDic = {}
            distritosDic[key] = listaCon2
            listaDistritos.append(distritosDic)
        for distrito in listaDistritos:
            for d in distrito:
                for c in distrito[d]:
                    for concelho1 in c:
                        for concelho2 in listaConcelhos:
                            for concelho3 in concelho2:
                                if concelho1 == concelho3:
                                    c.update(concelho2)
        return listaDistritos

def writeToFileAcentuados(file1,locaisAcentuados):
    f1 = open(file1,'w')
    json.dump(locaisAcentuados,f1,ensure_ascii=False, indent=4)

def writeToFileLocaisLimpos(file2,locaisSAcentuacao):
    f2 = open(file2,'w')
    json.dump(locaisSAcentuacao,f2,ensure_ascii=False, indent=4)


def execute():
   locaisAcentuados = createPlaces(main_file)
   writeToFileAcentuados(file1,locaisAcentuados)
   locaisSAcentuacao = removeAccentuation(locaisAcentuados)
   writeToFileLocaisLimpos(file2,locaisSAcentuacao) 

    