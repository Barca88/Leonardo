from flask import Flask, request,jsonify,Response
from flask_cors import CORS, cross_origin
from bson import ObjectId
import json
import mongo
## import init


## Flask  Requiring something from url .
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

####################### QUESTIONS ########################

@app.route('/imported_questions',methods=['GET']) # check
def listQuestions():
    return jsonify(mongo.listQuestions()) 

@app.route('/imported_questions/statsByAuthor/<id>',methods=['GET']) # check
def lookupAuthor(id):
    return jsonify(mongo.lookupAuthor(id)) 


@app.route('/imported_questions/statsByDomain/<id>',methods=['GET']) # check
def lookupDomain(id):
    return jsonify(mongo.lookupDomain(id)) 


@app.route('/imported_questions/statsByBoth/<author>/<domain>',methods=['GET']) # check
def lookupBoth(author,domain):
    return jsonify(mongo.lookupBoth(author,domain)) 


@app.route('/imported_questions',methods=['POST']) # check
def insertQuestion():
    question = request.get_json(force=True)
    mongo.insertQuestion(question)
    return jsonify('Inserted new question') 

@app.route('/imported_questions/<id>',methods=['PUT']) # check 
def editQuestion(id):
    question = request.get_json(force=True)
    mongo.editQuestion(id,question)
    return jsonify('Questão actualizada com sucesso ...') 

#########################################################

####################### ERRORS ########################
 
@app.route('/imported_errors',methods=['GET']) #check
def listErrors():
    return jsonify(mongo.listErrors()) 

@app.route('/imported_errors',methods=['POST'])  #check
def insertError():
    error = request.get_json(force=True)
    mongo.insertError(error)
    return jsonify('Inserted new error') 

#########################################################


####################### INFOS ########################
 
@app.route('/imported_info',methods=['GET']) # check
def listInfos():
    return jsonify(mongo.listInfos()) 

@app.route('/imported_info',methods=['POST']) # check 
def insertInfo():
    info = request.get_json(force=True)
    mongo.insertInfo(info)
    return jsonify('Inserted new info') 

#########################################################