#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, jsonify
from flask_login import LoginManager
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
###Imports
import datetime
from functools import wraps
import jwt
#########

login_manager = LoginManager()
mongo = PyMongo()
dadosFolio = {}
indexList = []
tags = []

def register_extensions(app):
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('base', 'home','users','folios','settings','analise','tagging','importacao','georreferenciacao','base','documentacao'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def apply_themes(app):
    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith('static'):
            themename = values.get('theme', None) or \
                app.config.get('DEFAULT_THEME', None)
            if themename:
                theme_file = "{}/{}".format(themename, values.get('filename', ''))
                if path.isfile(path.join(app.static_folder, theme_file)):
                    values['filename'] = theme_file
        return url_for(endpoint, **values)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/tommi"
    app.config['SECRET_KEY'] = 'tommi'
    mongo.init_app(app)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    apply_themes(app)
    return app


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            print("wrong len")
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            #data = jwt.decode(token, current_app.config['SECRET_KEY'])
            data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
            user = mongo.db.users.find_one({"_id":data['sub']})
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            did = ObjectId()
            reqstring= request.method + ":" + request.url
            if not user:
                raise RuntimeError('User not found')
            mongo.db.activeUsers.find_one_and_update({"_id":data['sub']},{"$set":{"_id":data['sub'],"stamp":date}},upsert=True)
            mongo.db.history.insert_one({"_id":did, "user":data['sub'], "stamp":date, "request":reqstring})
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            print("wrong token")
            return jsonify(invalid_msg), 401

    return _verify

def admin_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            #data = jwt.decode(token, current_app.config['SECRET_KEY'])
            data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
            user = mongo.db.users.find_one({"_id":data['sub'], "tipo":"Admin"})
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            did = ObjectId()
            reqstring= request.method + ":" + request.url
            if not user:
                raise RuntimeError('User or Administrator not found')
            mongo.db.activeUsers.find_one_and_update({"_id":data['sub']},{"$set":{"_id":data['sub'],"stamp":date}},upsert=True)
            mongo.db.history.insert_one({"_id":did, "user":data['sub'], "stamp":date, "request":reqstring})
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

def photo_auth(request, picName):
    auth_headers = request.headers.get('Authorization', '').split()

    token = auth_headers[1]
    #data = jwt.decode(token, current_app.config['SECRET_KEY'])
    data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
    user = mongo.db.users.find_one({"_id":data['sub']})
    if user:
        if user['tipo'] == 'Admin':
            return True
        elif user['_id'] == picName:
            return True
    return False