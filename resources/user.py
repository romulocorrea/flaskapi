# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.user import User
from resources.auth import auth, bcrypt


class UserCreateAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='You must provide your name', location='json')
        self.reqparse.add_argument('username', type=str, required=True, help='You must provide a valid username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide a valid password', location='json')
        super(UserCreateAPI, self).__init__()


    def hash_password(self, password):
        return bcrypt.generate_password_hash(password)


    def post(self):
        params = self.reqparse.parse_args()
        User(name=params['name'], username=params['username'], password=self.hash_password(params['password'])).save()
        return make_response(jsonify({'data': 'User created'}), 201)


class UserListAPI(Resource):
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='headers')
        self.reqparse.add_argument('username', type=str, required=True, help='You must provide a username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide a password', location='json')
        super(UserListAPI, self).__init__()


    def get(self):
        users = User.objects.all()
        return make_response(jsonify({'data': users}), 201)


class UserAPI(Resource):
    decorators = [auth.login_required]


    def get(self, id):
        user = User.objects(id=id)
        if not user or len(user) == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return make_response(jsonify({'data': user}), 201)
