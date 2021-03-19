#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask_pymongo import PyMongo


login_manager = LoginManager()
mongo = PyMongo()
dadosFolio = {}
indexList = []
tags = []


def register_extensions(app):
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('base', 'home','users','folios','settings','analise','importacao','base'):
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
    app.config['SECRET_KEY'] = 'Tommi'
    mongo.init_app(app)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    apply_themes(app)
    return app
