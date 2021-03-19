from flask import jsonify, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from app.analise import blueprint
from app import mongo

from bson.json_util import dumps
from bson.json_util import loads 

from flask_cors import CORS, cross_origin
CORS(blueprint)

import re
import time

@blueprint.route('/foliosnames', methods=['GET'])
def pesquisafolios():
    folios = mongo.db.folios.find({}, {"_id": 1})
    #for folio in folios:
     #   print(folio)
    return jsonify(loads(dumps(folios)))   

@blueprint.route('/folio/<folio>', methods=['GET'])
def showfolios(folio):
    folio = mongo.db.folios.find_one({"_id":folio})
    return jsonify(loads(dumps(folio)))  


@blueprint.route('/pesquisa', methods=['GET'])
def pesquisaresultados():
    palavra = request.args.get('pesquisa') 
    selectedFolio = request.args.get('selectedFolio') 
    tipo = request.args.get('tipo')
    versao = request.args.get('versao')
    resultado = request.args.get('resultado') 
    npalavras = 0
    # se especificou num de palavras
    if resultado == "npalavras": 
        npalavras = request.args.get('npalavras')
    
    if selectedFolio == "Todos": 
        res_pesquisa = procuraTextoTodos(palavra,versao, resultado,selectedFolio,npalavras) 
    else: 
        res_pesquisa = procuraTextoFolio(palavra,versao,selectedFolio,resultado,npalavras)
    
    return jsonify(loads(dumps(res_pesquisa)))

'''
def searchTypeOne(palavras): 
    for pal in palavras: 
        if pal.startswith("+") or pal.startswith("-") or pal.startswith("~") or pal.startswith('"') or pal.startswith("<") or pal.startswith(">"): 
           return False 
    return True   
'''

'''
# Retorna o tipo da pesquisa
def searchType(pesquisa):
    palavras = pesquisaIncludePalavra(pesquisa)
    if searchTypeOne(palavras): 
        return 1 
'''      

# split com o operador '+'
def pesquisaIncludePalavra(palavra):

    #elimina espaços no inicio e no fim da string
    #palavra = palavra.strip()
    if not(palavra.startswith('"')) :    
        x = palavra.split()
        return x
    else : 
        return palavra

                            
# Função chamada quando é necessário procurar em todos os fólios
def procuraTextoTodos(palavra, versao, resultado, folio, npalavras):
    resultados = [] 
    resposta = []
    res = [] 
    
    i = 0
    
    year, month, day, hour, minutes = map(int, time.strftime("%Y %m %d %H %M").split())

    data = str(year) + '-' + str(month) + '-' + str(day) 
    hora = str(hour) + ":" + str(minutes)

    doc = mongo.db.pesquisas.insert({'pesquisa': str(palavra), 'folio' : 'Todos', 'versao' : str(versao), 'resultado' : str(resultado), 'data' : str(data), 'hora' : str(hora) })

    folios = mongo.db.folios.find() 

    palavra = palavra.strip()
    pls = pesquisaIncludePalavra(palavra) 

    # pesquisa por tags
    if len(pls) == 2 and pls[0] == "+Tag": 
        tag = "<" + pls[1] + ">"  
        ftag = "</" + pls[1] + ">"
        #print(tag)
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
                            valor = re.search(str(tag), periodo)
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
                        valor = re.search(str(tag), linha)
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
                    exp = '([a-zà-úA-ZÀ-Ú0-9,\.\/\]\[]* ){'+ npalavras + '}'+ tag + '.*' + ftag + '[\/,)]? ([a-zà-úA-ZÀ-Ú0-9,\.\/\#\?\[\]]* ){'+ npalavras +'}'
                
                    for match in re.finditer(exp, linha):
                        novo = {
                            'idfolio': str(folio['_id']),
                            'linha': nlinhas,
                            'valor': match.group()
                        }
                        resultados.append(novo)
        
        print(resultados)
        
        if resultado == 'npalavras': 
            #print(resultados)
            return resultados 


        unique = { each['valor'] : each for each in resultados }.values()
        return resultados
                            

    if(resultado == 'periodo'):
        for folio in folios:
            
            if(folio['versao'] == versao or versao == 'todas'):
                nlinhas = 0
                linhas = folio['textoSTags'].split("\n")
                for linha in linhas:
                    nperiodos = 0
                    nlinhas += 1
                    periodos = linha.split(".")
                    
                    if not(palavra.startswith('"')) and not(palavra.endswith('"')):
                        
                        for pl in pls: 
                            #print(periodos)
                        
                            if pl.startswith("+"): 
                                # remove o carater + da pesquisa
                                pl_without = (pl[1:])  
                                #print(pl_without)
                                for periodo in periodos:
                                    nperiodos += 1
                                    valor = re.search(str(pl_without), periodo)
                                    valor2 = re.search(str("<" + pl_without + ">"),periodo) 
                                    valor3 = re.search(str("</" + pl_without + ">"),periodo)
                                    if(valor and not(valor2) and not(valor3)):
                                        novo = {
                                            'idfolio': str(folio['_id']),
                                            'linha': nlinhas,
                                            'periodo': nperiodos,
                                            'valor': periodo
                                        }    
                                        resultados.append(novo)  
                            

                            if not(pl.startswith("+")) and not(pl.startswith("-")): 
                                for periodo in periodos:
                                    nperiodos += 1
                                    valor = re.search(str(pl), periodo)
                                    valor2 = re.search(str("<" + pl + ">"),periodo) 
                                    valor3 = re.search(str("</" + pl + ">"),periodo)
                                    if(valor and not(valor2) and not(valor3)):
                                        novo = {
                                            'idfolio': str(folio['_id']),
                                            'linha': nlinhas,
                                            'periodo': nperiodos,
                                            'valor': periodo
                                        }    
                                        resultados.append(novo)            
                        
                            # não inclui palavra na pesquisa 
                            if pl.startswith("-"): 
                                # remove o carater - da pesquisa
                                pl_without = (pl[1:])  
                                #print(pl_without)
                                for res in resultados: 
                                    valor = re.search(str(pl_without),res['valor'])
                                    if valor:
                                        resultados.remove(res)
                    
                    else : 
                        # para tratar das pesquisa com "" onde precisa de fazer match exato
                        # remove o carter " no íncio e fim 
                        sem_aspas = palavra[1:-1]
                        for periodo in periodos:
                            nperiodos += 1
                            valor = periodo.find(sem_aspas) 
                            valor2 = re.search(str("<" + sem_aspas + ">"),periodo) 
                            valor3 = re.search(str("</" + sem_aspas + ">"),periodo)
                            if(valor!= -1 and not(valor2) and not(valor3)):
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
            
                    if not(palavra.startswith('"')) and not(palavra.endswith('"')):
                                
                        for pl in pls: 
                            #print(periodos)                          
                            if pl.startswith("+"): 
                                # remove o carater + da pesquisa
                                pl_without = (pl[1:])  
                                valor = re.search(str(pl_without), linha)
                                valor2 = re.search(str("<" + pl_without + ">"),linha) 
                                valor3 = re.search(str("</" + pl_without + ">"),linha)
                                if(valor and not(valor2) and not(valor3)):
                                    novo = {
                                        'idfolio': str(folio['_id']),
                                        'linha': nlinhas,
                                        'valor': linha
                                    }    
                                    resultados.append(novo)  
                            
                            if not(pl.startswith("+")) and not(pl.startswith("-")): 
                                pl_without = (pl[1:])  
                                valor = re.search(str(pl_without), linha)
                                valor2 = re.search(str("<" + pl_without + ">"),linha) 
                                valor3 = re.search(str("</" + pl_without + ">"),linha)
                                if(valor and not(valor2) and not(valor3)):
                                    novo = {
                                        'idfolio': str(folio['_id']),
                                        'linha': nlinhas,
                                        'valor': linha
                                    }    
                                    resultados.append(novo)  
                            
                            # não inclui palavra na pesquisa 
                            if pl.startswith("-"): 
                                # remove o carater - da pesquisa
                                pl_without = (pl[1:])  
                                #print(pl_without)
                                for res in resultados: 
                                    valor = re.search(str(pl_without),res['valor'])
                                    if valor:
                                        resultados.remove(res)
                    
                    else : 
             
                        # para tratar das pesquisa com "" onde precisa de fazer match exato
                        # remove o carter " no íncio e fim 
                        sem_aspas = palavra[1:-1]
                        valor = linha.find(sem_aspas)
                        valor2 = re.search(str("<" + sem_aspas + ">"),linha) 
                        valor3 = re.search(str("</" + sem_aspas + ">"),linha)
                        if(valor!= -1 and not(valor2) and not(valor3)):
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
                #print(linha)
                nlinhas += 1 
                #exp = '((\w+  ?){0,'+npalavras+'})(' + palavra + ')((  ?\w+){0,'+npalavras+'})'
                exp = '([a-zà-úA-ZÀ-Ú0-9,\.\/\]\[]* ){'+ npalavras + '}'+ palavra + '[\/,)]? ([a-zà-úA-ZÀ-Ú0-9,\.\/\#\?\[\]]* ){'+ npalavras +'}'
                
                for match in re.finditer(exp, linha):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': match.group()
                    }
                    resultados.append(novo)
                    
                
    if resultado == 'npalavras': 
       
        return resultados 
    
    unique = { each['valor'] : each for each in resultados }.values()
    return unique 
    

def procuraTextoFolio(palavra,versao,folio,resultado,npalavras):
    resultados = []
    

    year, month, day, hour, minutes = map(int, time.strftime("%Y %m %d %H %M").split())

    data = str(year) + '-' + str(month) + '-' + str(day) 
    hora = str(hour) + ":" + str(minutes)

    doc = mongo.db.pesquisas.insert({'pesquisa': str(palavra), 'folio' : str(folio), 'versao' : str(versao), 'resultado' : str(resultado), 'data' : str(data), 'hora' : str(hora) })


    folio = mongo.db.folios.find_one({"_id":folio})
    print(folio) 

    pls = pesquisaIncludePalavra(palavra) 
    
    # pesquisa por tags
    if len(pls) == 2 and pls[0] == "+Tag": 
        tag = "<" + pls[1] + ">" 
        ftag = "</" + pls[1] + ">" 
        
        if(resultado == 'periodo'):
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nperiodos = 0
                nlinhas += 1
                periodos = linha.split(".")
                for periodo in periodos:
                    nperiodos += 1
                    valor = re.search(str(tag), periodo)
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
                valor = re.search(str(tag), linha)
                if(valor):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': linha
                    }    
                    resultados.append(novo)  
        # mudar isto
        else:
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nlinhas += 1 
                exp = '([a-zà-úA-ZÀ-Ú0-9,\.\/\]\[]* ){'+ npalavras + '}'+ tag + '.*' + ftag + '[\/,)]? ([a-zà-úA-ZÀ-Ú0-9,\.\/\#\?\[\]]* ){'+ npalavras +'}'
                
                for match in re.finditer(exp, linha):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': match.group()
                    }
                    resultados.append(novo)

        #print(resultados)

        if resultado == 'npalavras': 
            return resultados 

        unique = { each['valor'] : each for each in resultados }.values()
        return unique 

    if(folio['versao'] == versao or versao == 'todas'):
        if(resultado == 'periodo'):
            nlinhas = 0
            linhas = folio['textoSTags'].split("\n")
            for linha in linhas:
                nperiodos = 0
                nlinhas += 1
                periodos = linha.split(".")
                
                if not(palavra.startswith('"')) and not(palavra.endswith('"')):
                    
                    for pl in pls: 
                        #print(periodos)
                    
                        if pl.startswith("+"): 
                            # remove o carater + da pesquisa
                            pl_without = (pl[1:])  
                            #print(pl_without)
                            for periodo in periodos:
                                nperiodos += 1
                                valor = re.search(str(pl_without), periodo)
                                valor2 = re.search(str("<" + pl_without + ">"),periodo) 
                                valor3 = re.search(str("</" + pl_without + ">"),periodo)
                                if(valor and not(valor2) and not(valor3)):
                                    novo = {
                                        'idfolio': str(folio['_id']),
                                        'linha': nlinhas,
                                        'periodo': nperiodos,
                                        'valor': periodo
                                    }    
                                    resultados.append(novo)  

                        if not(pl.startswith("+")) and not(pl.startswith("-")): 
                            for periodo in periodos:
                                nperiodos += 1
                                valor = re.search(str(pl), periodo)
                                valor2 = re.search(str("<" + pl + ">"),periodo) 
                                valor3 = re.search(str("</" + pl + ">"),periodo)
                                if(valor and not(valor2) and not(valor3)):
                                    novo = {
                                        'idfolio': str(folio['_id']),
                                        'linha': nlinhas,
                                        'periodo': nperiodos,
                                        'valor': periodo
                                    }    
                                    resultados.append(novo)            
                    
                        # não inclui palavra na pesquisa 
                        if pl.startswith("-"): 
                            # remove o carater - da pesquisa
                            pl_without = (pl[1:])  
                            #print(pl_without)
                            for res in resultados: 
                                valor = re.search(str(pl_without),res['valor'])
                                if valor:
                                    resultados.remove(res)
            
                else : 
                    # para tratar das pesquisa com "" onde precisa de fazer match exato
                    # remove o carter " no íncio e fim 
                    sem_aspas = palavra[1:-1]
                    for periodo in periodos:
                        nperiodos += 1
                        valor = periodo.find(sem_aspas)
                        valor2 = re.search(str("<" + sem_aspas + ">"),periodo) 
                        valor3 = re.search(str("</" + sem_aspas + ">"),periodo)
                        if(valor!= -1 and not(valor2) and not(valor3)):
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
                
                if not(palavra.startswith('"')) and not(palavra.endswith('"')):
                    
                    for pl in pls: 
                        #print(periodos)                          
                        if pl.startswith("+"): 
                            # remove o carater + da pesquisa
                            pl_without = (pl[1:])  
                            valor = re.search(str(pl_without), linha)
                            valor2 = re.search(str("<" + pl_without + ">"),linha) 
                            valor3 = re.search(str("</" + pl_without + ">"),linha)
                            if(valor and not(valor2) and not(valor3)):
                                novo = {
                                    'idfolio': str(folio['_id']),
                                    'linha': nlinhas,
                                    'valor': linha
                                }    
                                resultados.append(novo)  
                        
                        if not(pl.startswith("+")) and not(pl.startswith("-")): 
                            pl_without = (pl[1:])  
                            valor = re.search(str(pl_without), linha)
                            valor2 = re.search(str("<" + pl_without + ">"),linha) 
                            valor3 = re.search(str("</" + pl_without + ">"),linha)
                            if(valor and not(valor2) and not(valor3)):
                                novo = {
                                    'idfolio': str(folio['_id']),
                                    'linha': nlinhas,
                                    'valor': linha
                                }    
                                resultados.append(novo)  
                       
                        # não inclui palavra na pesquisa 
                        if pl.startswith("-"): 
                            # remove o carater - da pesquisa
                            pl_without = (pl[1:])  
                            #print(pl_without)
                            for res in resultados: 
                                valor = re.search(str(pl_without),res['valor'])
                                if valor:
                                    resultados.remove(res)
                    
                    else : 
                        # para tratar das pesquisa com "" onde precisa de fazer match exato
                        # remove o carter " no íncio e fim 
                        sem_aspas = palavra[1:-1]
                        valor = linha.find(sem_aspas)
                        valor2 = re.search(str("<" + sem_aspas + ">"),linha) 
                        valor3 = re.search(str("</" + sem_aspas + ">"),linha)
                        if(valor != -1 and not(valor2) and not(valor3)):
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
                exp = '([a-zà-úA-ZÀ-Ú0-9,\.\/\]\[]* ){'+ npalavras + '}'+ palavra + '[\/,)]? ([a-zà-úA-ZÀ-Ú0-9,\.\/\#\?\[\]]* ){'+ npalavras +'}'
           
                for match in re.finditer(exp, linha):
                    novo = {
                        'idfolio': str(folio['_id']),
                        'linha': nlinhas,
                        'valor': match.group()
                    }
                    resultados.append(novo)
    
    if resultado == 'npalavras': 
        return resultados 
    
    unique = { each['valor'] : each for each in resultados }.values()
    return unique 