#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'documentacao_blueprint',
    __name__,
    url_prefix='/documentacao',
    template_folder='templates',
    static_folder='static'
)
