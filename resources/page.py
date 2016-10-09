# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.page import Page
from resources.auth import auth
from resources.commons import Commons


class PageListAPI(Resource):
    decorators = [auth.login_required]


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='You must provide a title', location='json')
        self.reqparse.add_argument('url', type=str, required=True, help='You must provide an url', location='json')
        self.reqparse.add_argument('categoryId', type=str, required=True, help='You must provide a category', location='json')
        super(PageListAPI, self).__init__()


    def get(self):
        pages = Page.objects.all() if auth.isAdmin() else Page.objects(userId=auth.user['id'])
        return Commons.notFound('page') if Commons.checkIfNotExists(pages) else make_response(jsonify({'data': pages}), 201)


    def post(self):
        params = self.reqparse.parse_args()
        Page(
            title=params['title'],
            url=params['url'],
            categoryId=params['categoryId'],
            userId=auth.user['id']
        ).save()
        return make_response(jsonify({'data': 'Page created'}), 201)


class PageAPI(Resource):
    decorators = [auth.login_required]


    def get(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            page = Page.objects(id=id)
            if Commons.checkIfNotExists(page):
                return Commons.notFound('page')
            else:
                Page.objects(id=id).update(views=page[0].views + 1)
                return make_response(jsonify({'data': page}), 201)
        return auth.unauthorized()


    def put(self, id):
        params = self.reqparse.parse_args()
        if auth.isValidId(id) and auth.isAuthorized(id):
            if Commons.checkIfNotExists(Page.objects(id=id)):
                return Commons.notFound('page')
            data = commons.filterQueryParams(params)
            Page.objects(id=id).update_one(upsert=False, write_concern=None, **data)
            return make_response(jsonify({'data': 'Page updated'}), 201)
        return auth.unauthorized()


    def delete(self, id):
        if auth.isValidId(id) and auth.isAuthorized(id):
            page = Page.objects(id=id)
            if Commons.checkIfNotExists(page):
                return Commons.notFound('page')
            page.delete()
            return make_response(jsonify({'data': 'Page was deleted'}), 201)
        return auth.unauthorized()
