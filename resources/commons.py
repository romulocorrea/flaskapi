# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import jsonify, make_response


class Commons(object):
    @classmethod
    def checkIfNotExists(self, param):
        return param == None or len(param) == 0

    @classmethod
    def notFound(self, param):
        return make_response(jsonify({'error': 'No such ' + param + ' was found'}), 404)

    @classmethod
    def filterQueryParams(self, params):
        data = {}
        for param in params:
            if params[param] != None:
                data.update({ param : params[param]})
        return data
