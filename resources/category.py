# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.category import Category
from models.page import Page
from resources.auth import auth
from resources.commons import Commons


class CategoryListAPI(Resource):
    '''This class is responsible for handling GET and POST requests from categories'''
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='You must provide a title', location='json')
        super(CategoryListAPI, self).__init__()


    def get(self):
        '''This method returns all categories from an user'''
        categories = Category.objects.all() if auth.isAdmin() else Category.objects(userId=auth.user['id'])
        return Commons.notFound('category') if Commons.checkIfNotExists(categories) else make_response(jsonify({'data': categories}), 201)


    def post(self):
        '''This method creates a new category related to an user'''
        params = self.reqparse.parse_args()
        Category(
            title=params['title'],
            userId=auth.user['id']
        ).save()
        return make_response(jsonify({'data': 'Category created'}), 201)


class CategoryAPI(Resource):
    '''This class is responsible for handling GET, PUT and DELETE requests for a single category'''
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='You must provide a title', location='json')
        super(CategoryAPI, self).__init__()


    def get(self, id):
        '''This method receives an ID from an category and returns the category'''
        if Commons.isValidId(id):
            category = Category.objects(id=id)
            if Commons.checkIfNotExists(category):
                return Commons.notFound('category')
            if auth.isAuthorized(category[0].userId):
                return make_response(jsonify({'data': category}), 201)
        return auth.unauthorized()


    def put(self, id):
        '''This method receives an ID from an category and updates the category'''
        if Commons.isValidId(id):
            category = Category.objects(id=id)
            if Commons.checkIfNotExists(category):
                return Commons.notFound('category')
            if auth.isAuthorized(category[0].userId):
                params = Commons.filterQueryParams(self.reqparse.parse_args())
                Category.objects(id=id).update_one(upsert=False, write_concern=None, **params)
                return make_response(jsonify({'data': 'Category updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        '''This method receives an ID from an category and deletes the category'''
        if Commons.isValidId(id):
            category = Category.objects(id=id)
            if Commons.checkIfNotExists(category):
                return Commons.notFound('category')
            if auth.isAuthorized(category[0].userId):
                category.delete()
                return make_response(jsonify({'data': 'Category was deleted'}), 201)
        return auth.unauthorized()


class CategoryPagesAPI(Resource):
    '''This class is responsible for handling GET requests for pages from a category'''
    decorators = [auth.login_required]


    def get(self, id):
        if Commons.isValidId(id):
            pages = Page.objects(categoryId=id)
            if Commons.checkIfNotExists(pages):
                return Commons.notFound('page')
            if auth.isAuthorized(pages[0].userId):
                return make_response(jsonify({'data': pages}), 201)
        return auth.unauthorized()
