#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'quiz_blueprint',
    __name__,
    url_prefix='/api/v0',
    template_folder='templates',
    static_folder='static'
)