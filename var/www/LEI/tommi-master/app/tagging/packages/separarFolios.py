#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os

main_file = 'Tommi-Folios-S1.txt' 

def cleanTexto(texto):
    texto = re.sub(r'\n',' ',texto)
    texto = re.sub(r'’',r"'",texto)
    texto = re.sub(r'(\[\d+\w+?\])',r'\n\n\1\n',texto)
    return texto

def criaNome(s):
    s = re.sub(r'\[','./Folios/Folio',s)
    s = re.sub(r'\]','.txt',s)
    os.makedirs(os.path.dirname(s),exist_ok=True)
    return s

def createFolio(texto):
    titulos = re.findall(r'\[\d+\w+?\]',texto)
    folios = texto.split('\n\n')
    for t in titulos:
        for folio in folios:
            if t in folio:
                nome = criaNome(t)
                f = open(nome, "w")
                f.write(folio)
                f.close()

def readFile():
    f = open(main_file, "r")
    texto = f.read()
    return texto


def execute():
    texto = readFile()
    texto = cleanTexto(texto)
    createFolio(texto)

    
    

        

