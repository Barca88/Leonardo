#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'generator_blueprint',
    __name__,
    url_prefix='/generator',
    template_folder='templates',
    static_folder='static'
)
