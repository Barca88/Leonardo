#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask_pymongo import PyMongo
from app import login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app import mongo
from app.base.models import User
import re

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.pesquisa'))

@blueprint.route('/home')
def pesquisa():
    folios = mongo.db.folios.find()
    return render_template('pesquisa/pesquisa.html',folios=folios)

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

@blueprint.route('/pesquisar', methods=['POST'])
def route_template_pesquisar():
    palavra = request.form.get('procurar')
    tipo = request.form.get('tipo')
    versao = request.form.get('versao')
    folio = request.form.get('folio')
    resultado = request.form.get('resultado')
    npalavras = request.form.get('npalavras')
    resultados = {}

    if(tipo == 'texto'):
        resultados = procuraTexto(palavra,versao,folio,resultado,npalavras)
        return render_template('pesquisa/res_texto.html', resultados=resultados, palavra=palavra)
    else:
        resultados = procuraTag(palavra,folio)
        return render_template('pesquisa/res_tag.html', resultados=resultados, palavra=palavra)


@blueprint.route('/admin')
def route_default_login():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


## Login & Registration
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if request.method == "POST":
        if 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            user = mongo.db.users.find_one({"email":email})
            if user and check_password_hash(user["password"], password):
                login_user(User(user["email"]))
                return redirect(url_for('home_blueprint.index',nome=user['_id']))
            return render_template('errors/page_403.html')
    else:
        if request.method == "GET":
            return render_template(
                'login/login.html',
                login_form=login_form,
                create_account_form=create_account_form
            )
        return redirect(url_for('base_blueprint.route_default'))



@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

    

## Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500