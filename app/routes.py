# -*- coding: utf-8 -*-
#!flask/bin/python


from flask_restful import Api
from resources.auth import AuthAPI
from resources.register import UserCreateAPI
from resources.user import UserListAPI, UserAPI
# from resources.page import PageAPI, PageListAPI
# from resources.category import CategoryAPI, CategoryListAPI


def register(app):
    api = Api(app)

    api.add_resource(AuthAPI, '/api/v1/login', endpoint='login')
    api.add_resource(UserCreateAPI, '/api/v1/register', endpoint='register')

    api.add_resource(UserAPI, '/api/v1/user/<id>', endpoint='user')
    api.add_resource(UserListAPI, '/api/v1/users', endpoint='users')

    # api.add_resource(CategoryAPI, '/api/v1/category/<id>', endpoint='category')
    # api.add_resource(CategoryListAPI, '/api/v1/categories', endpoint='categories')

    # api.add_resource(PageAPI, '/api/v1/page/<id>', endpoint='page')
    # api.add_resource(PageListAPI, '/api/v1/pages', endpoint='pages')
