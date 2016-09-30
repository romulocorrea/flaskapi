# -*- coding: utf-8 -*-
#!flask/bin/python

from flask import abort, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_httpauth import HTTPTokenAuth
from flask_bcrypt import Bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from models.user import User
from app.config import schema, secret
auth = HTTPTokenAuth(scheme=schema)
bcrypt = Bcrypt()


@auth.verify_token
def verify_token(token):
    s = Serializer(secret)
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


class AuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='Username is required', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='Password is required', location='json')
        super(AuthAPI, self).__init__()


    def verify_password(self, hash, password):
        try:
            bcrypt.check_password_hash(hash, password)
        except:
            return False
        return True


    def generate_auth_token(self, user, expiration=3600):
        s = Serializer(secret, expires_in=expiration)
        return s.dumps({'id': str(user[0].id)})


    def post(self):
        params = self.reqparse.parse_args()
        user = User.objects(username=params['username'])
        if len(user) == 0:
            return make_response(jsonify({'error': 'User not found'}), 404)
        if self.verify_password(user[0].password, params['password']) != True:
            return make_response(jsonify({'error': 'Incorrect password'}), 403)
        token = self.generate_auth_token(user)
        return make_response(jsonify({'data': token}), 201)
