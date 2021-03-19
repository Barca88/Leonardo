#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'import_blueprint',
    __name__,
    url_prefix='/import',
    template_folder='templates',
    static_folder='static'
)
