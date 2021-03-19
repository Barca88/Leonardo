#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'packages_blueprint',
    __name__,
    static_folder='static'
)
