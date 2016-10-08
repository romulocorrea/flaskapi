# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.user import User
from resources.auth import auth, bcrypt


def checkIfNotExists(param):
    return param == None or len(param) == 0


def notFound(self):
    return make_response(jsonify({'error': 'No user was found'}), 404)


class UserListAPI(Resource):
    decorators = [auth.login_required]


    def get(self):
        users = User.objects.all() if auth.isAdmin() else User.objects(id=auth.user['id'])
        return notFound() if checkIfNotExists(users) else make_response(jsonify({'data': users}), 201)


class UserAPI(Resource):
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()


    def get(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            user = User.objects(id=id)
            return notFound() if checkIfNotExists(user) else make_response(jsonify({'data': user}), 201)
        return auth.unauthorized()


    def put(self, id):
        params = self.reqparse.parse_args()
        if auth.isValidId(id) and auth.isAuthorized(id):
            user = User.objects(id=id)
            if checkIfNotExists(user):
                return notFound()
            else:
                data = {}
                for param in params:
                    if params[param] != None:
                        data.update({ param : params[param]})
                User.objects(id=id).update_one(upsert=False, write_concern=None, **data)
                return make_response(jsonify({'data': 'User info updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            user = User.objects(id=id)
            if checkIfNotExists(user):
                return notFound()
            else:
                user.delete()
                return make_response(jsonify({'data': 'User was deleted'}), 201)
        return auth.unauthorized()
