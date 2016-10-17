# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import abort, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as JWT, BadSignature, SignatureExpired)
from models.user import User
from app.config import config
auth = HTTPTokenAuth(scheme=config['authSchema'])
bcrypt = config['bcrypt']


@auth.verify_token
def verify_token(token):
    jwt = JWT(config['secret'])
    try:
        data = jwt.loads(token)
        auth.user = data
    except SignatureExpired:
        abort(403)
    except BadSignature:
        abort(403)
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def hash_password(password):
    return bcrypt.generate_password_hash(password)


def isAdmin():
    return hasattr(auth, 'user') and auth.user['profile'] == 'ADMIN'


def isSameUser(userId):
    return hasattr(auth, 'user') and str(auth.user['id']) == str(userId)


def isAuthorized(userId):
    return isAdmin() or isSameUser(userId)


auth.hash_password = hash_password
auth.isAdmin = isAdmin
auth.isSameUser = isSameUser
auth.isAuthorized = isAuthorized
auth.unauthorized = unauthorized


class AuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='Username is required', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='Password is required', location='json')
        super(AuthAPI, self).__init__()


    @classmethod
    def verify_password(self, hash, password):
        return bcrypt.check_password_hash(hash, password)


    @classmethod
    def generate_auth_token(self, user, expiration=3600):
        jwt = JWT(config['secret'], expires_in=expiration)
        return jwt.dumps({
            'id': str(user[0].id),
            'profile': str(user[0].profile)
        })


    def post(self):
        params = self.reqparse.parse_args()
        user = User.objects(username=params['username'])
        if len(user) == 0 or len(user) > 1:
            return make_response(jsonify({'error': 'User not found'}), 404)
        elif self.verify_password(user[0].password, params['password']) != True:
            return make_response(jsonify({'error': 'Incorrect password'}), 403)
        return make_response(jsonify({'data': self.generate_auth_token(user)}), 201)
