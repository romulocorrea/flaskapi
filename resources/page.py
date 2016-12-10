# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.page import Page
from resources.auth import auth
from resources.commons import Commons


class PageListAPI(Resource):
    '''This class is responsible for handling GET and POST requests from pages'''
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='You must provide a title', location='json')
        self.reqparse.add_argument('url', type=str, required=True, help='You must provide an url', location='json')
        self.reqparse.add_argument('categoryId', type=str, required=True, help='You must provide a category', location='json')
        super(PageListAPI, self).__init__()


    def get(self):
        '''This method returns all pages from an user'''
        pages = Page.objects.all() if auth.isAdmin() else Page.objects(userId=auth.user['id'])
        return Commons.notFound('page') if Commons.checkIfNotExists(pages) else make_response(jsonify({'data': pages}), 201)


    def post(self):
        '''This method creates a new page related to an user'''
        params = self.reqparse.parse_args()
        if Commons.isValidId(params['categoryId']):
            Page(
                title=params['title'],
                url=params['url'],
                categoryId=params['categoryId'],
                userId=auth.user['id']
            ).save()
            return make_response(jsonify({'data': 'Page created'}), 201)
        return make_response(jsonify({'error': 'Invalid categoryId'}), 500)


class PageAPI(Resource):
    '''This class is responsible for handling GET, PUT and DELETE requests for a single page'''
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('url', type=str, location='json')
        self.reqparse.add_argument('categoryId', type=str, location='json')
        super(PageAPI, self).__init__()


    def get(self, id):
        '''This method receives an ID from an page and returns the page'''
        if Commons.isValidId(id):
            page = Page.objects(id=id)
            if Commons.checkIfNotExists(page):
                return Commons.notFound('page')
            if auth.isAuthorized(page[0].userId):
                Page.objects(id=id).update(views=page[0].views + 1)
                return make_response(jsonify({'data': page}), 201)
        return auth.unauthorized()


    def put(self, id):
        '''This method receives an ID from an page and updates the page'''
        params = self.reqparse.parse_args()
        if Commons.isValidId(id):
            page = Page.objects(id=id)
            if Commons.checkIfNotExists(page):
                return Commons.notFound('page')
            if auth.isAuthorized(page[0].userId):
                data = Commons.filterQueryParams(params)
                Page.objects(id=id).update_one(upsert=False, write_concern=None, **data)
                return make_response(jsonify({'data': 'Page updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        '''This method receives an ID from an page and deletes the page'''
        if Commons.isValidId(id):
            page = Page.objects(id=id)
            if Commons.checkIfNotExists(page):
                return Commons.notFound('page')
            if auth.isAuthorized(page[0].userId):
                page.delete()
                return make_response(jsonify({'data': 'Page was deleted'}), 201)
        return auth.unauthorized()
