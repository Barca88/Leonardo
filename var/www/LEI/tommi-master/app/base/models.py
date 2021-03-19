#!/usr/bin/python
# -*- coding: utf-8 -*-

from bcrypt import gensalt, hashpw
from flask_login import UserMixin

from app import mongo, login_manager

class User(UserMixin):
    def __init__(self,username):
        self._id = username

    def __repr__(self):
        return str(self._id)

    def get_id(self):
        return self._id

    @login_manager.user_loader
    def user_loader(email):
        user = mongo.db.users.find_one({"email":email})
        return User(user) if user else None
