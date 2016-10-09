# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.category import Category
from resources.auth import auth
from resources.commons import Commons


class CategoryListAPI(Resource):
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='You must provide a title', location='json')
        super(CategoryListAPI, self).__init__()


    def get(self):
        categories = Category.objects.all() if auth.isAdmin() else Category.objects(userId=auth.user['id'])
        return Commons.notFound('category') if Commons.checkIfNotExists(categories) else make_response(jsonify({'data': categories}), 201)


    def post(self):
        params = self.reqparse.parse_args()
        Category(
            title=params['title'],
            userId=auth.user['id']
        ).save()
        return make_response(jsonify({'data': 'Category created'}), 201)


class CategoryAPI(Resource):
    decorators = [auth.login_required]


    def get(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            category = Category.objects(id=id)
            return Commons.notFound('category') if Commons.checkIfNotExists(category) else make_response(jsonify({'data': category}), 201)
        return auth.unauthorized()


    def put(self, id):
        params = self.reqparse.parse_args()
        if auth.isValidId(id) and auth.isAuthorized(id):
            if Commons.checkIfNotExists(Category.objects(id=id)):
                return Commons.notFound('category')
            data = commons.filterQueryParams(params)
            Category.objects(id=id).update_one(upsert=False, write_concern=None, **data)
            return make_response(jsonify({'data': 'Category updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            category = Category.objects(id=id)
            if Commons.checkIfNotExists(category):
                return Commons.notFound('category')
            category.delete()
            return make_response(jsonify({'data': 'Category was deleted'}), 201)
        return auth.unauthorized()
