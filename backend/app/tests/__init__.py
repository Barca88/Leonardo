#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'tests_blueprint',
    __name__,
    url_prefix='/tests',
    template_folder='templates',
    static_folder='static'
)
