from flask import Flask, request,jsonify,Response
from flasgger import swag_from, Swagger
from flask_cors import CORS, cross_origin
from bson import ObjectId
import settings
import json
import mongo
import init


## Flask  Requiring something from url .
app = Flask(
        __name__,
        static_url_path='',
        static_folder='docs')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
swagger = Swagger(app,
  template= {
    "swagger": "3.0",
    "openapi": "3.0.0",
    "info": {
        "title": "Leonardo Importações",
        "version": "2.0.0",
    }
  }
)
####################### QUESTIONS ########################
@app.route('/imported_questions', methods=['GET']) # check
@swag_from('docs/questions/listQuestions.yml')
def listQuestions():
    return jsonify(mongo.listQuestions())

@app.route('/imported_questions/statsByAuthor/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupAuthor.yml')
def lookupAuthor(id):
    return jsonify(mongo.lookupAuthor(id))


@app.route('/imported_questions/statsByDomain/<id>',methods=['GET']) # check
@swag_from('docs/questions/lookupDomain.yml')
def lookupDomain(id):
    return jsonify(mongo.lookupDomain(id))


@app.route('/imported_questions/statsByBoth/<author>/<domain>',methods=['GET']) # check
@swag_from('docs/questions/lookupBoth.yml')
def lookupBoth(author,domain):
    return jsonify(mongo.lookupBoth(author,domain))


@app.route('/imported_questions',methods=['POST']) # check
@swag_from('docs/questions/insertQuestion.yml')
def insertQuestion():
    question = request.get_json(force=True)
    mongo.insertQuestion(question)
    return jsonify('Inserted new question')

@app.route('/imported_questions/<id>',methods=['PUT']) # check
@swag_from('docs/questions/editQuestion.yml')
def editQuestion(id):
    question = request.get_json(force=True)
    mongo.editQuestion(id,question)
    return jsonify('Questão actualizada com sucesso ...')

#########################################################

####################### ERRORS ########################

@app.route('/imported_errors',methods=['GET']) #check
@swag_from('docs/errors/listErrors.yml')
def listErrors():
    return jsonify(mongo.listErrors())

@app.route('/imported_errors',methods=['POST'])  #check
@swag_from('docs/errors/insertError.yml')
def insertError():
    error = request.get_json(force=True)
    mongo.insertError(error)
    return jsonify('Inserted new error')

#########################################################


####################### INFOS ########################

@app.route('/imported_info',methods=['GET']) # check
@swag_from('docs/info/listInfos.yml')
def listInfos():
    return jsonify(mongo.listInfos())

@app.route('/imported_info',methods=['POST']) # check
@swag_from('docs/info/insertInfo.yml')
def insertInfo():
    info = request.get_json(force=True)
    mongo.insertInfo(info)
    return jsonify('Inserted new info')

#########################################################




####################### DOMAINS ########################

@app.route('/domains',methods=['GET']) # check
@swag_from('docs/domains/listDomains.yml')
def listDomains():
    return jsonify(mongo.listDomains())


#########################################################


app.run(debug=settings.FLASK_DEBUG, port=settings.FLASK_PORT)