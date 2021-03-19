#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.home import blueprint
from flask import render_template,request
from flask_login import login_required
from app import dadosFolio
import os
from app import mongo

@blueprint.route('/index')
@login_required
def index():
    folios = mongo.db.folios.count()
    users = mongo.db.users.count()
    indices = mongo.db.indexacao.count()
    tags = mongo.db.tags.count()
    settings = mongo.db.settings.count()
    nome = request.args.get('nome')
    return render_template('index.html',nome=nome,users=users, folios=folios, indices=indices,tags=tags,settings=settings)


