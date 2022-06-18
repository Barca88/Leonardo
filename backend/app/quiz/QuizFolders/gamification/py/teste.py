import sys
import collections 
import operator
import pymongo
from pymongo import MongoClient

num = "A78478"

#MONGODB
myclient = MongoClient('mongodb://localhost:27017')

dblist = myclient.list_database_names()

mydb = myclient["leo"]
mycol = mydb["alunos"]

for x in mycol.find({"numero": num}):
  print(1)

#CARTAS:

total_de_tempo = 190 #ms
total_de_certas = x.get("total_de_perguntas_certas") #ms
total_de_erradas = x.get("total_de_perguntas_erradas") #ms
tempo_do_quiz = 270 #ms
tempo_da_resposta = 90 #é mudado para cada pergunta
tempo_da_pergunta = 100 #é mudado para cada pergunta
valor = "true" #é mudado para cada pergunta -> true/false
#o streak e o streak total vai ser adicionado nas variaveis do backlog

#NIVEL:

nivel_da_pergunta = 1 #é mudado para cada pergunta -> 1..5
valor 
#o streak e o streak total vai ser adicionado nas variaveis do backlog

#RANKING:

nivel_atual = x.get("nivel") #1..5
ranking_atual = 100 #1..nº de alunos
ranking = {"João": 221, "Fabio": 43, "Marcia": 31, "Joana": 124, "Tiago": 32, "Miguel": 0} #lista do ranking

#BACK LOG:

backlog = 0 #nº de respostas certas ou erradas consecutivas
limite_backlog = 5
#numero_de_backlogs = 0 #nº de vezes q o backlog atinge o limite do backlog


Aluno = collections.namedtuple('Aluno',['nome', 'nivel', 'xp', 'rank', 'certas', 'erradas', 'backlog', 'n_backlog', 'cartas'])

user = Aluno(x.get("nome"), nivel_atual, x.get("EXP_atual"), 5, total_de_certas, total_de_erradas,0,x.get("melhor_sequencia"), x.get("coleção_de_cartas"))

#print("INCIO:")
print(user)
#print(ranking)
#print("///////////////////////////////////////////////////////////////////")
#print("APOS O MODULO")

def ranking_por_pergunta(fRanking, fUser):
    fRanking.update({fUser[0] : int(fUser[2])})
    fRanking = sorted(fRanking.items(), key=operator.itemgetter(1), reverse=True)
    print(fRanking)

def levels(fUser):
    if int(fUser[2]) <= 9 and int(fUser[2]) >= 0:
        fUser = fUser._replace(nivel = "1")
    if int(fUser[2]) <= 24 and int(fUser[2]) >= 10:
        fUser = fUser._replace(nivel = "2")
    if int(fUser[2]) <= 44 and int(fUser[2]) >= 25:
        fUser = fUser._replace(nivel = "3")
    if int(fUser[2]) <= 69 and int(fUser[2]) >= 45:
        fUser = fUser._replace(nivel = "4")
    if int(fUser[2]) >= 70:
        fUser = fUser._replace(nivel = "5")
    return fUser
     
def nivel_por_pergunta(fUser, fValor, fNivel_da_pergunta, fRanking):
    if fValor == "true":
        fUser = fUser._replace(xp = str(int(fUser[2]) + fNivel_da_pergunta))
        fUser = fUser._replace(backlog = fUser[6] + 1)
        fUser = fUser._replace(certas = str(int(fUser[4])+1))
        fUser = levels(fUser)
    else:
        fUser = fUser._replace(backlog = 0)
        fUser = fUser._replace(erradas = str(int(fUser[5])+1))
    fRanking = ranking_por_pergunta(fRanking,fUser)
    return fUser, fRanking

def backlog_por_pergunta(fUser, fBacklog):
    if fUser[6] >= fBacklog:
        fUser = fUser._replace(n_backlog = str(int(fUser[7])+1))
    return fUser

def carta_por_pergunta(fUser):
    if tempo_da_resposta < (tempo_da_pergunta * 0.5):
        if tempo_da_resposta > (tempo_da_pergunta * 0.25):
            fUser[8].append('Sonic Racoon')
        else:
            fUser[8].append('Flash Racoon')
    else:
        if tempo_da_resposta < (tempo_da_pergunta * 0.75):
            fUser[8].append('Ninja Racoon')
        else:
            fUser[8].append('Reverse Flash Racoon')
    
    if valor == "true":
        fUser[8].append('DumbleRacoon')
    else:
        fUser[8].append('Racoon')

    if total_de_certas > total_de_erradas:
        if total_de_certas - total_de_erradas == total_de_certas:
            fUser[8].append('XavieRacoon')
        else: 
            fUser[8].append('GandRacoon')
    else:
        fUser[8].append('Racoon')
    
    if fUser[7] > 5 :
        fUser[8].append('Iron-Racoon')
    
    return fUser

def update_aluno(fUser):
    myquery = { "numero": num }
    newvalues = { "$set": { "nivel": fUser[1], "EXP_atual": fUser[2], "total_de_perguntas_certas": fUser[4], "total_de_perguntas_erradas": fUser[5], "melhor_sequencia": fUser[7], "coleção_de_cartas":fUser[8]} }
    mycol.update_one(myquery, newvalues)
    print(fUser)

user, ranking = nivel_por_pergunta(user, valor, nivel_da_pergunta, ranking)
user = backlog_por_pergunta(user, backlog)
#user = carta_por_pergunta(user)
update_aluno(user)

print(user)
print(ranking)
for x in mycol.find():
  print(x)

