# -*- coding: utf-8 -*-
#!flask/bin/python

from flask_pymongo import PyMongo

def DBConnect(app):
    app.config['MONGO_HOST'] = 'ds041486.mlab.com'
    app.config['MONGO_PORT'] = 41486
    app.config['MONGO_USERNAME'] = 'admin'
    app.config['MONGO_PASSWORD'] = 'admin'
    app.config['MONGO_DBNAME'] = 'dev-web-flask'
    return PyMongo(app, config_prefix='MONGO')
