# -*- coding: utf-8 -*-
#!flask/bin/python

from flask_mongoengine import MongoEngine
db = MongoEngine()


secret = 'mysupersecretkey'
# settings = {
#     'db': 'dev-web-flask',
#     'host': 'ds041566.mlab.com',
#     'port': 41566,
#     'username': 'admin',
#     'password': 'admin'
# }
# settings = {
#     'db': 'dev-web-flask',
#     'host': 'localhost',
#     'port': 27017
# }
settings = {
    'db': 'dev-web',
    'host': '52.39.177.184',
    'port': 27017,
    'username': 'admin',
    'password': 'admin'
}
schema = 'Token'
