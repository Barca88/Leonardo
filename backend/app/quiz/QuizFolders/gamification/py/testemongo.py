import sys
import collections 
import operator
import pymongo
from datetime import date
from pymongo import MongoClient
from random import randrange
import json

num = "A78478"

#MONGODB
myclient = MongoClient('mongodb://localhost:27017')

dblist = myclient.list_database_names()
mydb = myclient["leo"]
mycol = mydb["alunos"]
mycolAdmin = mydb["leoadmin"]
mycolQuestion = mydb["questions"]

with open('json_test.json') as f:
  data = json.load(f)

def levels(x):
    if int(x.get("EXP_atual")) <= 9 and int(x.get("EXP_atual")) >= 0:
        return 1
    if int(x.get("EXP_atual")) <= 24 and int(x.get("EXP_atual")) >= 10:
        return 2
    if int(x.get("EXP_atual")) <= 44 and int(x.get("EXP_atual")) >= 25:
        return 3
    if int(x.get("EXP_atual")) <= 69 and int(x.get("EXP_atual")) >= 45:
        return 4
    return 5

def tempo_da_pergunta(time_pergunta, time_resposta):
  a=0
  b=0
  c=0
  d=0

  if time_resposta < ((time_pergunta/60) * 0.5):
    if time_resposta < ((time_pergunta/60) * 0.25):
      c = 1
    a = 1
  else:
    if time_resposta > ((time_pergunta/60) * 0.75):
      d = 1
    b = 1
  return a,b,c,d

def carta_por_pergunta(tempo_da_resposta, tempo_da_pergunta, x, val):
    list=[] 
    if tempo_da_resposta < (tempo_da_pergunta * 0.5):
        if tempo_da_resposta > (tempo_da_pergunta * 0.25):
            list.append('Sonic Racoon')
        else:
            list.append('Flash Racoon')
    else:
        if tempo_da_resposta < (tempo_da_pergunta * 0.75):
            list.append('Ninja Racoon')
        else:
            list.append('Reverse Flash Racoon')
    
    if val == "1":
        list.append('DumbleRacoon')
    else:
        list.append('Racoon')
    
    if int(x.get("melhor_sequencia")) > 5 :
        list.append('Iron-Racoon')
    
    return list
  
def cartas_finais(cartas, li, df):
    for x in cartas:
      if x not in li:
        li.append(x)
        day = date.today()
        df.append(str(day))
    return li, df


def update_aluno(x , nom, dom, val, time_pergunta, time_resposta):
    myquery = { "nome": nom, "dominio": dom}
    level = levels(x)
    aux_c = 0
    aux_e = 0
    backlog = 0
    backlogNeg = 0
    seq = 0
    semResp = 0
    seqNeg = 0
    day = date.today()
    if val == "1":
      aux_c = 1
      backlog = int(x.get("sequencia_atual")) + 1
      backlogNeg = 0
    elif val == "0":
      aux_e = 1
      backlog = 0
      backlogNeg = int(x.get("pior_seq")) + 1
    else:
      aux_e = 1
      backlog = 0
      backlogNeg = int(x.get("pior_seq")) + 1
      semResp = int(x.get("total_de_perguntas_sem_resposta")) + 1
    if( int(x.get("melhor_sequencia")) < backlog ):
      seq = backlog
    if( int(x.get("pior_seq")) < backlogNeg ):
      seqNeg = backlogNeg
    cartas = carta_por_pergunta(time_pergunta, time_resposta, x, val)
    li = list(x.get("coleção_de_cartas"))
    df = list(x.get("data_das_cartas"))
    final, data_final = cartas_finais(cartas,li,df)
    a,b,c,d = tempo_da_pergunta(time_pergunta, time_resposta)
    newvalues = { "$set": { "total_de_perguntas_sem_resposta": str(semResp), "pior_seq": str(seqNeg),"ultima_sessao": str(day), "melhor_sequencia": str(seq), "sequencia_atual": str(backlog), "nivel": str(level),"EXP_atual": str(int(x.get("EXP_atual")) + (aux_c - aux_e)), "total_de_perguntas_certas": str(aux_c + int(x.get("total_de_perguntas_certas"))), "total_de_perguntas_erradas": str(aux_e + int(x.get("total_de_perguntas_erradas"))), "total_de_perguntas_+50%": str(int(x.get("total_de_perguntas_+50%")) + b), "total_de_perguntas_-50%": str(int(x.get("total_de_perguntas_-50%")) + a),"total_de_perguntas_+75%": str(int(x.get("total_de_perguntas_+75%")) + d),"total_de_perguntas_-25%": str(int(x.get("total_de_perguntas_-25%")) + c), "coleção_de_cartas":final, "data_das_cartas":data_final, "total_perguntas": str(int(x.get("total_de_perguntas_erradas")) + int(x.get("total_de_perguntas_certas")))} }
    mycol.update_one(myquery, newvalues)

def update_admin():
  x = 0
  y = 0
  for x in mycolAdmin.find():
    print("ola")
    uti = 0
    p_certas = 0 
    p_erradas = 0
    p_total = 0
    t_acerto = 0
    n_cartas = 0
    for y in mycol.find({"dominio": x.get("dominio")}):
      uti += 1
      p_certas += int(y.get("total_de_perguntas_certas"))
      p_erradas += int(y.get("total_de_perguntas_erradas"))
      p_total += int(y.get("total_perguntas"))
      n_cartas += len(y.get("coleção_de_cartas"))
    t_acerto = (p_certas/p_total) * 100
    newvalues = {"$set": { "utilizadores": str(uti), "sessoes": str(uti), "tpMedSessao": "0", "questoes": str(p_total), "taxaAcerto": str(t_acerto), "cartas": str(n_cartas)}}
    myquery = {"dominio": x.get("dominio")}
    mycolAdmin.update_one(myquery, newvalues)

def criar_frase(respondidas, acerto, erro, x):
  acerto_perc = (acerto * 100) / respondidas
  erro_perc = (erro * 100) / respondidas
  val_1 = randrange(4)
  if (val_1 == 0):
    val = randrange(4)
    if(val == 0):
      print(str(acerto) + " acertaram esta pergunta")
    if(val == 1):
      print("A percentagem de acerto é " + str(acerto_perc))
    if(val == 2):
      print(str(erro) + " erraram esta pergunta")
    if(val == 3):
      print("A percentagem de erro é " + str(erro_perc))
  if (val_1 == 1):
    mel_seq = x.get("melhor_sequencia")
    pior_seq = x.get("pior_seq")
    atual_seq = x.get("sequencia_atual")
    if(int(atual_seq) <= int(mel_seq)/2):
      print("Já tens uma sequencia certa bastante elevada, tenta continuar assim")
    if(int(atual_seq) == int(mel_seq)):
      print("Se acertares esta pergunta atinges a tua sequencia certa mais elevada")
    if(int(atual_seq) <= int(pior_seq)/2):
      print("Já tens uma sequencia errada bastante elevada, tenta acerta para pergunta para não aumentar ainda mais")
    if(int(atual_seq) == int(pior_seq)):
      print("Se errares esta pergunta atinges a tua sequencia errada mais elevada")
  if (val_1 == 2):
    li = list(x.get("coleção_de_cartas"))
    if ("Sonic Racoon" not in li):
      print("Se responderes a esta pergunta em menos de metade do tempo ganhas a carta Sonic Racoon")
    if ("Iron-Racoon" not in li):
      print("Já quase toda a gente tem a carta Iron-Racoon, tenta responder a esta pergunta correta para teres a mesma carta")
    if ("Ninja Racoon" not in li):
      print("Nao erres esta pergunta, senão vais ganhar a carta Ninja Racoon")
    if ("Racoon" not in li):
      print("Cuidado com o tempo, mais um bocado e vais receber a carta Racoon")
  if (val_1 == 3):
    alunos = mycol.find().sort("EXP_atual")
    alunos_antes = mycol.find().sort("EXP_atual")
    alunos_depois = mycol.find().sort("EXP_atual")
    num = 1
    antes = 1
    depois = 1
    EXP = 0
    EXP_antes = 0
    EXP_depois = 0

    ## GUARDAR VARIAVEIS PARA O MENOS E DEPOIS PARA PERCORRER SO UMA VEZ
    
    for aluno in alunos:
      if( EXP == 0): 
        num += 1
        if(aluno.get("nome") == x.get("nome")):
          EXP = aluno.get("EXP_atual")
    
    for aluno in alunos_antes:
      antes += 1
      if(antes == num - 1):
        if(num != 1):
          EXP_antes = aluno.get("EXP_atual")
          break
    
    for aluno in alunos_depois: 
      depois += 1
      if depois == num + 1: 
        if num < 15:
          EXP_depois = aluno.get("EXP_atual")
          break

    if( EXP == EXP_antes):
      print("Se acertares esta pergunta sobes para uma posição no ranking")
    if( EXP == EXP_depois):
      print("Se errares esta pergunta desces uma posição no ranking")
    if( antes == 1 and EXP == EXP_antes):
      print("Se acertares esta pergunta ficas em numero 1 do ranking")
    if( depois == 15 and EXP == EXP_depois):
      print("Se errares esta pergunta desces para o ultimo lugar do ranking")
    

## RANKING/SEQUENCIAS/CARTAS/HIBRIDOS    +/- 4 para cada uma destas

# Criar constantes para nao ter as frases escritas no codigo
# Ver o despacho da reitoria para ver o template para a dissertação
# Falar com o Jaime

# Ranking: DONE
  # "Se acertares esta pergunta sobes para uma posição no ranking"
  # "Se errares esta pergunta desces uma posição no ranking"
  # "Se acertares esta pergunta ficas em numero 1 do ranking"
  # "Se errares esta pergunta desces para o ultimo lugar do ranking"

# Sequencias: DONE
  # "Se acertares esta pergunta atinges a tua sequencia certa mais elevada"
  # "Se errares esta pergunta atinges a tua sequencia errada mais elevada"
  # "Já tens uma sequencia certa bastante elevada, tenta continuar assim"
  # "Já tens uma sequencia errada bastante elevada, tenta acerta para pergunta para não aumentar ainda mais"

# Cartas: DONE
  # "Se responderes a esta pergunta em menos de metade do tempo ganhas a carta X"
  # "Já quase toda a gente tem a carta X, tenta responder a esta pergunta correta para teres a mesma carta"
  # "Nao erres esta pergunta, senão vais ganhar a carta X"
  # "Cuidado com o tempo, mais um bocado e vais receber a carta X"

# Percentagens de erro: COMPLETAR O TEXTO
  # "X acertaram esta pergunta"
  # "X erraram esta pergunta"
  # "A percentagem de acerto é X"
  # "A percentagem de erro é X"

def update_question(x, respondidas, certas, erradas, val):
  respondidas_atual = respondidas + 1
  certas_atual = certas
  erradas_atual = erradas
  if (val == "1" ):
    certas_atual = certas + 1
  else: 
    erradas_atual = erradas + 1
  newvalues = { "$set": { "question_respondidas": respondidas_atual, "question_certas": certas_atual, "question_erradas": erradas_atual}}
  myquery = {"questionid": x.get("questionid")}
  mycolQuestion.update_one(myquery, newvalues)


## QUIZ -> avaliador pergunta se a GAM quer dar um incentivo para um X utilizador -> Receber um identificador do utilizador
## e analisar o seu historial de GAM -> Como decidir o incentivo?? -> Com base no icentivo gerar um incentivo aleatorio -> 
## enviar o icentivo para o QUIZ

"""
def iter():
  for pergunta in data['perguntas']:
    x = 0
    for x in mycol.find({"nome": pergunta['user']['name'], "dominio": pergunta['question']['domain']}):
      if x.get("nome") == pergunta['user']['name'] and x.get("dominio") == pergunta['question']['domain']:
          update_aluno(x, x.get("nome"),x.get("dominio"),pergunta['answer']['correction'], int(pergunta['question']['answering_time']), int(pergunta['answer']['answer_time']))
    if(x == 0):
      mydict = {"nome": pergunta['user']['name'],"dominio":pergunta['question']['domain'] ,"imagem": "", "numero": "", "nivel": "1" , "EXP_atual": "0" , "total_de_perguntas_certas": "0" , "total_de_perguntas_erradas": "0", "total_de_perguntas_+50%": "0", "total_de_perguntas_-50%": "0", "total_de_perguntas_+75%": "0", "total_de_perguntas_-25%": "0", "melhor_sequencia": "0", "total_de_quizes_certos": "0", "total_de_quizes_positivos": "0", "total_de_quizes_negativos": "0", "coleção_de_cartas":"", "data_das_cartas":"", "sequencia_atual": "0", "total_perguntas": "0", "ultima_sessao": "", "pior_seq": "0", "total_de_perguntas_sem_resposta": "0", "tpTotalQuiz": "0", "tpMedSes": "0", "tmMedPer": "0"}
      mycol.insert_one(mydict)
    y = 0
    for y in mycolQuestion.find({"questionid": pergunta['question']['questionid']}):
      update_question(y, y.get("question_respondidas"),y.get("question_certas"),y.get("question_erradas"), pergunta['answer']['correction'])
      criar_frase(y.get("question_respondidas"),y.get("question_certas"),y.get("question_erradas"), x)
    if (y == 0):
      mydict = {
                "questionid": pergunta['question']['questionid'],
                "scholarity": pergunta['question']['scholarity'],
                "domain": pergunta['question']['domain'],
                "subdomain": pergunta['question']['subdomain'],
                "subsubdomain": pergunta['question']['subsubdomain'],
                "question_respondidas": 0,
                "question_certas": 0,
                "question_erradas": 0
              }
      mycolQuestion.insert_one(mydict)
      print("adicionado")
    
  update_admin()
"""

def iter(pre_resposta, pos_resposta):
  if (pos_resposta == []):
    for x in mycol.find({"nome": pre_resposta[nome], "dominio": pre_resposta[dominio]}):
      for y in mycolQuestion.find({"questionid": pre_resposta[id]}):
        criar_frase(y.get("question_respondidas"),y.get("question_certas"),y.get("question_erradas"), x)
  else:
    for x in mycol.find({"nome": pos_resposta[nome], "dominio": pos_resposta[dominio]}):
      if x.get("nome") == pos_resposta[nome] and x.get("dominio") == pos_resposta[dominio]:
          update_aluno(x, x.get("nome"),x.get("dominio"),pos_resposta['correction'], int(pos_resposta['answering_time']), int(pos_resposta['answer_time']))
    if(x == 0):
      mydict = {"nome": pos_resposta[nome],"dominio":pos_resposta[dominio] ,"imagem": "", "numero": "", "nivel": "1" , "EXP_atual": "0" , "total_de_perguntas_certas": "0" , "total_de_perguntas_erradas": "0", "total_de_perguntas_+50%": "0", "total_de_perguntas_-50%": "0", "total_de_perguntas_+75%": "0", "total_de_perguntas_-25%": "0", "melhor_sequencia": "0", "total_de_quizes_certos": "0", "total_de_quizes_positivos": "0", "total_de_quizes_negativos": "0", "coleção_de_cartas":"", "data_das_cartas":"", "sequencia_atual": "0", "total_perguntas": "0", "ultima_sessao": "", "pior_seq": "0", "total_de_perguntas_sem_resposta": "0", "tpTotalQuiz": "0", "tpMedSes": "0", "tmMedPer": "0"}
      mycol.insert_one(mydict)
     y = 0
    for y in mycolQuestion.find({"questionid": pos_resposta['questionid']}):
      update_question(y, y.get("question_respondidas"),y.get("question_certas"),y.get("question_erradas"), pos_resposta['correction'])
    if (y == 0):
      mydict = {
                "questionid": pos_resposta['questionid'],
                "scholarity": pos_resposta['scholarity'],
                "domain": pos_resposta['domain'],
                "subdomain": pos_resposta['subdomain'],
                "subsubdomain": pos_resposta['subsubdomain'],
                "question_respondidas": 0,
                "question_certas": 0,
                "question_erradas": 0
              }
      mycolQuestion.insert_one(mydict)
      print("adicionado")
    
  update_admin()


iter()

for x in mycol.find({}):
  print(x.get("nome") + "-> " + x.get("total_de_perguntas_certas")+ "-> " + x.get("total_de_perguntas_erradas") + "-> " + x.get("total_de_perguntas_+50%") + "-> " + x.get("total_de_perguntas_-50%") + "-> " + x.get("total_de_perguntas_+75%") + "-> " + x.get("total_de_perguntas_-25%") + "->" + x.get("melhor_sequencia") + "->" + str(x.get("coleção_de_cartas")) + " " + x.get("dominio") + " " + x.get("sequencia_atual") + " " + str(x.get("data_das_cartas")))