# -*- coding: utf-8 -*-
#!flask/bin/python

import json
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, jsonify, make_response, abort
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config import DBConnect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
auth = HTTPTokenAuth(scheme='Token')
bcrypt = Bcrypt(app)
connection = DBConnect(app)


@auth.verify_token
def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        abort(403)
    except BadSignature:
        abort(403)
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


def toJSON(data):
    return json.loads(json_util.dumps(data))


class AuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='You must provide a username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide a password', location='json')
        super(AuthAPI, self).__init__()


    def verify_password(self, hash, password):
        try:
            bcrypt.check_password_hash(hash, password)
        except:
            return False
        return True


    def generate_auth_token(self, user, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': user['_id']})


    def post(self):
        params = self.reqparse.parse_args()
        auth = {
            'username' : params['username'],
            'password' : params['password']
        }
        user = toJSON(connection.db.users.find_one({'username': auth['username']}))
        if user == None:
            return make_response(jsonify({'error': 'User not found'}), 404)
        if self.verify_password(user['password'], auth['password']) != True:
            return make_response(jsonify({'error': 'Incorrect password'}), 403)
        return make_response(jsonify({'token': self.generate_auth_token(user)}), 201)


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
        return toJSON(connection.db.users.find())


    def post(self):
        params = self.reqparse.parse_args()
        user = {
            'username' : params['username'],
            'password' : params['password']
        }

        if len(user['password']) < 8:
            return make_response(jsonify({'error': 'Your password must be at least 8 characters'}), 400)
        if connection.db.users.find_one({'username': user['username']}) != None:
            return make_response(jsonify({'error': 'This username has already been registered'}), 400)
        user['password'] = self.hash_password(user['password'])
        connection.db.users.insert_one(user);
        return make_response(jsonify({'success': 'User created'}), 201)


class UserAPI(Resource):
    decorators = [auth.login_required]


    def get(self, id):
        try:
            id = ObjectId(str(id))
        except:
            id = None
        user = toJSON(connection.db.users.find_one({ '_id' : id }))
        if not user or len(user) == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return {'user': user}


api = Api(app)
api.add_resource(AuthAPI, '/api/v1/auth', endpoint='auth')
api.add_resource(UserAPI, '/api/v1/users/<id>', endpoint='user')
api.add_resource(UserListAPI, '/api/v1/users', endpoint='users')


if __name__ == '__main__':
    app.run()
