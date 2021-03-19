#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'settings_blueprint',
    __name__,
    url_prefix='/settings',
    template_folder='templates',
    static_folder='static'
)
