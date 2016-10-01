# -*- coding: utf-8 -*-
#!flask/bin/python


from flask import Flask, jsonify, make_response
from app.config import config, db, initBcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret']
app.config['MONGODB_SETTINGS'] = config['dbSettings']
initBcrypt(app)
db.init_app(app)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


from app.routes import register
register(app)


if __name__ == '__main__':
    app.run()
