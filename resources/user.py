# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.user import User
from resources.auth import auth
from resources.commons import Commons


class UserCreateAPI(Resource):
    '''This class is responsible for handling POST requests for creating an user'''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='You must provide your name', location='json')
        self.reqparse.add_argument('username', type=str, required=True, help='You must provide a valid username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide a valid password', location='json')
        super(UserCreateAPI, self).__init__()


    def post(self):
        '''This method receives by params in the request`s headers the user`s data and saves it to the database'''
        params = self.reqparse.parse_args()
        User(
            name=params['name'],
            username=params['username'],
            password=auth.hash_password(params['password'])
        ).save()
        return make_response(jsonify({'data': 'User created'}), 201)


class UserListAPI(Resource):
    '''This class is responsible for handling GET requests for a list of users'''
    decorators = [auth.login_required]


    def get(self):
        users = User.objects.all() if auth.isAdmin() else User.objects(id=auth.user['id'])
        return Commons.notFound('user') if Commons.checkIfNotExists(users) else make_response(jsonify({'data': users}), 201)


class UserAPI(Resource):
    '''This class is responsible for handling GET, PUT and DELETE requests for a single user'''
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()


    def get(self, id):
        '''This method receives an ID from an user and returns the user'''
        if Commons.isValidId(id) and auth.isAuthorized(id):
            user = User.objects(id=id)
            return Commons.notFound('user') if Commons.checkIfNotExists(user) else make_response(jsonify({'data': user}), 201)
        return auth.unauthorized()


    def put(self, id):
        '''This method receives an ID from an user and updates the user'''
        params = self.reqparse.parse_args()
        if Commons.isValidId(id) and auth.isAuthorized(id):
            if Commons.checkIfNotExists(User.objects(id=id)):
                return Commons.notFound('user')
            data = commons.filterQueryParams(params)
            if data.has_key('password'):
                data['password'] = auth.hash_password(data['password'])
            User.objects(id=id).update_one(upsert=False, write_concern=None, **data)
            return make_response(jsonify({'data': 'User info updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        '''This method receives an ID from an user and deletes the user'''
        if Commons.isValidId(id) and auth.isAuthorized(id):
            user = User.objects(id=id)
            if Commons.checkIfNotExists(user):
                return Commons.notFound('user')
            user.delete()
            return make_response(jsonify({'data': 'User was deleted'}), 201)
        return auth.unauthorized()
