# -*- coding: utf-8 -*-
#!flask/bin/python


from app.config import db


class Category(db.Document):
    title = db.StringField(required=True, max_length=30)
    userId = db.ObjectIdField(required=True)
