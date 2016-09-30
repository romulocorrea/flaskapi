# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.user import User
from resources.auth import auth, bcrypt


class UserListAPI(Resource):
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='headers')
        self.reqparse.add_argument('username', type=str, required=True, help='You must provide a username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide a password', location='json')
        super(UserListAPI, self).__init__()


    def hash_password(self, password):
        return bcrypt.generate_password_hash(password)


    def get(self):
        users = User.objects.all()
        return make_response(jsonify({'data': users}), 201)


    def post(self):
        params = self.reqparse.parse_args()
        if not params['username'] or len(params['username']) < 5:
            return make_response(jsonify({'error': 'You must provide an username with at least 5 characters long'}), 400)
        elif not params['password'] or len(params['password']) < 5:
            return make_response(jsonify({'error': 'Your password must be at least 5 characters long'}), 400)
        elif len(User.objects(username=params['username'])) > 0:
            return make_response(jsonify({'error': 'This username has already been registered'}), 400)
        else:
            User(username=params['username'], password=self.hash_password(params['password'])).save()
            return make_response(jsonify({'data': 'User created'}), 201)


class UserAPI(Resource):
    decorators = [auth.login_required]


    def get(self, id):
        user = User.objects(id=id)
        if not user or len(user) == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        print user
        return make_response(jsonify({'data': user}), 201)
