# -*- coding: utf-8 -*-
#!flask/bin/python


import datetime
from app.config import db


class Page(db.Document):
    title = db.StringField(required=True, unique=True, max_length=30)
    url = db.URLField(required=True)
    views = db.IntField(default=0)
    likes = db.IntField(default=0)
    created = DateTimeField(default=datetime.datetime.now)
    categoryId = db.StringField(required=True)
    userId = db.StringField(required=True)