#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'stats_blueprint',
    __name__,
    url_prefix='/stats',
    template_folder='templates',
    static_folder='static'
)
