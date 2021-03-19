#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from app.analise import blueprint
from flask import render_template, request, flash
from flask_login import login_required
from app import mongo
from os import path, remove
from werkzeug.security import generate_password_hash
import datetime
import re
import json
import ast



import sys



@blueprint.route('/')
@login_required
def route_template():
    folios = mongo.db.folios.find()
    nome = request.args.get('nome')
    return render_template('analise.html', folios=folios,nome=nome)


def procuraTextoTodos(palavra, versao, resultado,npalavras):
    resultados = []
    folios = mongo.db.folios.find()
    if(resultado == 'periodo'):
        for folio in folios:
            if(folio['versao'] == versao or versao == 'todas'):
                nlinhas = 0
                linhas = folio['textoSTags'].split("\n")
                for linha in linhas:
                    nperiodos = 0
                    nlinhas += 1
                    periodos = linha.split(".")
                    for periodo in periodos:
                        nperiodos += 1
                        valor = re.search(palavra, periodo)
                        if(valor):
                            novo = {
                                'idfolio': str(folio['_id']),
                                'linha': nlinhas,
                                'periodo': nperiodos,
                                'valor': periodo
                            }
                            resultados.append(novo)
    elif(resultado == 'linha'):
            for folio in folios:
                if(folio['versao'] == versao or versao == 'todas'):
                    nlinhas = 0
                    linhas = folio['textoSTags'].split("\n")
                    for linha in linhas:
                        nlinhas += 1
                        valor = re.search(palavra, linha)
                        if(valor):
                            novo = {
                                'idfolio': str(folio['_id']),
                                'linha': nlinhas,
                                'valor': linha
                                }
                            resultados.append(novo)
    else:
        for folio in folios:
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nlinhas += 1 
                exp = '((\w+  ?){0,'+npalavras+'})(' + palavra + ')((  ?\w+){0,'+npalavras+'})'
                valor = re.findall(exp,linha)
                if(valor):
                    tuplo = valor[0]
                    tamanho = len(tuplo)
                    novo_resultado = tuplo[0] + palavra + tuplo[tamanho-1]
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': novo_resultado
                        }
                    resultados.append(novo)
    return resultados
   

def procuraTextoFolio(palavra,versao,folio,resultado,npalavras):
    resultados = []
    if(folio['versao'] == versao or versao == 'todas'):
        if(resultado == 'periodo'):
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nperiodos = 0
                nlinhas += 1
                periodos = linha.split(".")
                for periodo in periodos:
                    nperiodos += 1
                    valor = re.search(palavra, periodo)
                    if(valor):
                        novo = {
                            'idfolio': str(folio['_id']),
                            'linha': nlinhas,
                            'periodo': nperiodos,
                            'valor': periodo
                        }
                        resultados.append(novo)
        elif(resultado == 'linha'):
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nlinhas += 1
                valor = re.search(palavra, linha)
                if(valor):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': linha
                    }
                    resultados.append(novo)
        else:
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nlinhas += 1 
                exp = '((\w+  ?){0,'+npalavras+'})(' + palavra + ')((  ?\w+){0,'+npalavras+'})'
                valor = re.findall(exp,linha)
                if(valor):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': valor
                    }
                    resultados.append(valor)
    return resultados

        


def procuraTexto(palavra, versao, idfolio, resultado,npalavras):
    resultados = []
    if(idfolio == 'Todos'):
        resultados = procuraTextoTodos(palavra,versao,resultado,npalavras)
    else:
        folio = mongo.db.folios.find_one({"_id":idfolio})
        resultados = procuraTextoFolio(palavra,versao,folio,resultado,npalavras)
    return(resultados)



def procuraTagTodos(palavra):
    resultados = []
    tags = mongo.db.tags.find()
    for tag in tags:
        conteudo = tag['conteudoTag']
        for key,valores in conteudo.items():
            for valor in valores:
                if valor == palavra:
                    idtag = str(tag['_id'])
                    novo = {
                        'idfolio': key,
                        'tag': idtag
                    }
                    resultados.append(novo)
    return resultados


def procuraTag(palavra,idFolio):
    resultados = []
    resultados = procuraTagTodos(palavra)
    return resultados





@blueprint.route('/procurar', methods=['POST'])
@login_required
def route_template_procurar():
    palavra = request.form.get('procurar')
    tipo = request.form.get('tipo')
    versao = request.form.get('versao')
    folio = request.form.get('folio')
    resultado = request.form.get('resultado')
    npalavras = request.form.get('npalavras')
    resultados = {}
    nome = request.args.get('nome')

    if(tipo == 'texto'):
        resultados = procuraTexto(palavra,versao,folio,resultado,npalavras)
        return render_template('resultadosTexto.html', resultados=resultados, palavra=palavra,nome=nome)
    else:
        resultados = procuraTag(palavra,folio)
        return render_template('resultadosTag.html', resultados=resultados, palavra=palavra,nome=nome)

    
