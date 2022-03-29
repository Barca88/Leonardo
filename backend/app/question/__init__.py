#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'question_blueprint',
    __name__,
    url_prefix='/question',
    template_folder='templates',
    static_folder='static'
)