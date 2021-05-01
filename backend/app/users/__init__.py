#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'users_blueprint',
    __name__,
    url_prefix='/users',
    template_folder='templates',
    static_folder='static'
)