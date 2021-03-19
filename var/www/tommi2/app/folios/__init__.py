#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'folios_blueprint',
    __name__,
    url_prefix='/folios',
    template_folder='templates',
    static_folder='static'
)
