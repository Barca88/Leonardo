from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flasgger import Swagger
import sys
import os
import subprocess
import settings

app = Flask(__name__)
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
cors = CORS(app, resources={r"/text": {"origins": "http://localhost:1338"}})

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route('/text',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def text():
    """Importação de Questões.
    Importação das questões num formato anotado (.leo)
    ---
    tags:
      - Questões
    requestBody:
        description: Questão a publicar
        required: true
        content:
            text/plain:
                schema:
                    $ref: '#/definitions/Questão'
    definitions:
      Questão:
          type: object
          properties:
            question:
              type: file
              required: true

    responses:
      200:
        description: Importação da questão realizada com sucesso .

      500:
        description: Erro .
    """

    if request.method == 'POST':
       # Store .leo text and get it ready to be converted
       content = request.get_data()
       # Get path of program to be ran
       path = os.getcwd() + "/scripts/mkleonardo.py"
       result = subprocess.run(["python3", path],stdout = subprocess.PIPE, input=content)
       # Return the json
       answer = "[" + result.stdout.decode('utf-8') + "]"

    return answer

app.run(debug=settings.FLASK_DEBUG, port=settings.FLASK_PORT)