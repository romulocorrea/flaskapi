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
    '''This method is responsible for handling and validating tokens'''
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
    '''This method is responsible for creating 403 unauthorized errors'''
    return make_response(jsonify({'error': '403'}), 403)


def hash_password(password):
    '''This method is responsible for hashing the passwords'''
    return bcrypt.generate_password_hash(password)


def isAdmin():
    '''This method is responsible for verifying if an user is ADMIN'''
    return hasattr(auth, 'user') and auth.user['profile'] == 'ADMIN'


def isSameUser(userId):
    '''This method is responsible for verifying if the user requesting some action is the same user logged in'''
    return hasattr(auth, 'user') and str(auth.user['id']) == str(userId)


def isAuthorized(userId):
    '''This method is responsible for verifying if the user has access for some feature'''
    return isAdmin() or isSameUser(userId)


auth.hash_password = hash_password
auth.isAdmin = isAdmin
auth.isSameUser = isSameUser
auth.isAuthorized = isAuthorized
auth.unauthorized = unauthorized


class AuthAPI(Resource):
    '''This class is responsible for handling POST requests to logging in an user'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='Username is required', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='Password is required', location='json')
        super(AuthAPI, self).__init__()


    @classmethod
    def verify_password(self, hash, password):
        '''This method is responsible for validating the password'''
        return bcrypt.check_password_hash(hash, password)


    @classmethod
    def generate_auth_token(self, user, expiration=3600):
        '''This method is responsible for generating an auth token'''
        jwt = JWT(config['secret'], expires_in=expiration)
        return jwt.dumps({
            'id': str(user[0].id),
            'profile': str(user[0].profile),
            'name': str(user[0].name),
            'username': str(user[0].username)
        })


    def post(self):
        '''This method is responsible for handling POST requests from loggin forms'''
        params = self.reqparse.parse_args()
        user = User.objects(username=params['username'])
        if len(user) == 0 or len(user) > 1:
            return make_response(jsonify({'error': '404_USER'}), 404)
        elif self.verify_password(user[0].password, params['password']) != True:
            return make_response(jsonify({'error': '403_PASSWORD'}), 403)
        return make_response(jsonify({'data': self.generate_auth_token(user)}), 200)
