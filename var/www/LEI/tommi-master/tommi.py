#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_migrate import Migrate
from os import environ
from sys import exit
from config import config_dict
from app import create_app,mongo



get_config_mode = environ.get('GENTELELLA_CONFIG_MODE', 'Production')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid GENTELELLA_CONFIG_MODE environment variable entry.')

app = create_app(config_mode)
