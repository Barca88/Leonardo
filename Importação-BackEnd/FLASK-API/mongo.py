#!usr/bin/python3

# Importação dos módulos
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json

""" 
The code bellow will connect on the default host and port.
We also can can change that to specified the host and port:
	 client = MongoClient('localhost',27017)
Or use the MongoDB URI format: 
	 client = Mongoclient('mongodb://localhost:27017')
"""
client = MongoClient()

"""
A single instance of MongoDB can support multiple independent 
databases. When working with PyMongo you acess databases using
attributes style acess on MongoClient instances:
"""
# Select the leonardo in database 
leonardo = client.leonardo

# Select the work collection in leonardo database .
questions = leonardo.imported_questions
domains = leonardo.domains
errors = leonardo.imported_errors 
infos = leonardo.imported_info

################## QUESTIONS ########################
## Devolve a lista de Questions
def listQuestions():
	return list(questions.find({},{'_id':0}))

## Devolve a lista de Questions por Author
def lookupAuthor(author:str):
	return list(questions.find({'author':author},{'_id':0}))


## Devolve a lista de Questions por Domínio
def lookupDomain(domain:str):
	return list(questions.find({'domain':domain},{'_id':0}))


## Devolve a lista de Questions por Domínio
def lookupBoth(author:str,domain:str):
	return list(questions.find({'author':author,'domain':domain},{'_id':0}))

## Permite inserir uma question
def insertQuestion(question):
	 questions.insert_one(question)


## Permite editar a flag de uma question
def editQuestion(id,question):
	questions.find_one_and_update({'id':id},{'$set': {'flag':question['flag']}},upsert=True)

################## DOMAINS ########################
## Permite obter a lista de domínios

def listDomains()->list:
    return list(domains.find({},{'_id':0}))

################## ERRORS ########################

## Devolve a lista de Errors 
def listErrors():
	return list(errors.find({},{'_id':0}))


## Permite inserir um erro 
def insertError(error):
	error['id']= len(listErrors())
	errors.insert_one(error)

################## INFOS ########################

## Devolve a lista de infos 
def listInfos():
	return list(infos.find({},{'_id':0}))

## Permite inserir uma info 
def insertInfo(info):
	infos.insert_one(info)
