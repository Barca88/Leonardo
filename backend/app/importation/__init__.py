#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'importation_blueprint',
    __name__,
    url_prefix='/importation',
    template_folder='templates',
    static_folder='static'
)