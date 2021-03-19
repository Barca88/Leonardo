#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'tagging_blueprint',
    __name__,
    url_prefix='/tagging',
    static_folder='static'
)
