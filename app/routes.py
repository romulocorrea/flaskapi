# -*- coding: utf-8 -*-
#!flask/bin/python


from flask_restful import Api
from resources.auth import AuthAPI
from resources.user import UserCreateAPI, UserListAPI, UserAPI


def register(app):
    api = Api(app)
    api.add_resource(AuthAPI, '/api/v1/login', endpoint='login')
    api.add_resource(UserAPI, '/api/v1/users/<id>', endpoint='user')
    api.add_resource(UserListAPI, '/api/v1/users', endpoint='users')
    api.add_resource(UserCreateAPI, '/api/v1/register', endpoint='register')
