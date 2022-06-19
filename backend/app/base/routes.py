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
from app import login_manager, create_app, token_required, write_log
from app.base import blueprint
#from app.base.forms import LoginForm, CreateAccountForm
from app import mongo
#from app.base.models import User
import re

# este é meu
import json
from bson import json_util
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import jwt
CORS(blueprint)
#######


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.pesquisa'))


@blueprint.route('/home')
def pesquisa():
    
    folios = mongo.db.folios.find()
    return render_template('pesquisa/pesquisa.html', folios=folios)


@blueprint.route('/admin')
def route_default_login():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


####### Login & Registration###############################
@blueprint.route('/login', methods=['POST'])
def login():
    print('logggiiiin')
    _id = request.form.get('id')
    password = request.form.get('password')
    user = mongo.db.users.find_one({"_id": _id})
    if user and check_password_hash(user["password"], password):
        #users = [doc for doc in mongo.db.users.find()]
        #nome = request.args.get('nome')

        token = jwt.encode(dict(sub=_id, iat=datetime.utcnow(), exp=datetime.utcnow() + timedelta(minutes=15)),
                           # jwt app.config['SECRET_KEY']
                           '\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i', algorithm='HS256')
        
        write_log(_id, 'Login', '', 'successfull')
        write_log(_id, 'Home' , '', 'successfull')
        #return json_util.dumps({'token': token, 'user': user, 'users': users, 'nome': nome})
        return json_util.dumps({'token': token, 'user': user})
    else:
        write_log(_id,  'Login', '', 'failed')
        return json_util.dumps({'error': 'O utilizador não existe!'})


@blueprint.route('/logout', methods=['POST'])
@token_required
# @login_required
def logout():
    # logout_user()
    print("logging out")
    _id = request.form.get('id')
    user = mongo.db.users.find_one({"_id": _id})
    write_log(_id , 'Logout', '', 'successfull')
    return json_util.dumps({'message': 'Logged out!'})


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
