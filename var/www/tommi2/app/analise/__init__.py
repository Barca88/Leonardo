#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'analise_blueprint',
    __name__,
    url_prefix='/analise',
    template_folder='templates',
    static_folder='static'
)
