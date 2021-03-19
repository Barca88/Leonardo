#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import Email

## login and registration


class LoginForm(FlaskForm):
    email = TextField('Email', id='email',validators=[Email('Introduzir um email válido.')])
    password = PasswordField('Palavra-passe', id='pwd_login')


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create')
    email = TextField('Email',id='email')
    password = PasswordField('Password', id='pwd_create')
