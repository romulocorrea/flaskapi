# -*- coding: utf-8 -*-
#!flask/bin/python


from app.config import db


class User(db.Document):
    name = db.StringField(required=True, max_length=50)
    username = db.StringField(required=True, unique=True, max_length=15)
    password = db.StringField(required=True)