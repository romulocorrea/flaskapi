# -*- coding: utf-8 -*-
#!flask/bin/python


from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
db = MongoEngine()


config = {
    'bcrypt': Bcrypt(),
    'secret': 'mysupersecretkey',
    'dbSettings': {
        'db': 'dev-web',
        'host': '52.39.177.184',
        'port': 27017,
        'username': 'admin',
        'password': 'admin'
    },
    'authSchema': 'Token'
}


def initBcrypt(app):
    config['bcrypt'] = Bcrypt(app)