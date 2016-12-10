# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response
from bson.objectid import ObjectId


class Commons(object):
    '''This class is responsible for abstracting common methods'''
    @classmethod
    def checkIfNotExists(self, param):
        '''This method is responsible for checking if a param exists'''
        return param == None or len(param) == 0


    @classmethod
    def notFound(self, param):
        '''This method is responsible for generating 404 not found error'''
        return make_response(jsonify({'error': 'No such ' + param + ' was found'}), 404)


    @classmethod
    def filterQueryParams(self, params):
        '''This method is responsible for filtering query params'''
        data = {}
        for param in params:
            if params[param] != None:
                data.update({ param : params[param]})
        return data


    @classmethod
    def isValidId(self, data):
        '''This method is responsible for verifying if an ID is valid'''
        return ObjectId.is_valid(data)
