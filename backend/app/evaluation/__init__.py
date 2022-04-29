#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'evaluation_blueprint',
    __name__,
    url_prefix='/evaluation',
    template_folder='templates',
    static_folder='static'
)
