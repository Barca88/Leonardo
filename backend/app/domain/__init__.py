#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'domain_blueprint',
    __name__,
    url_prefix='/domain',
    template_folder='templates',
    static_folder='static'
)