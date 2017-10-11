#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from flask import Flask, request

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
basicauth = HTTPBasicAuth()
auth = HTTPTokenAuth(scheme='Token')

from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from app.controllers import default
from app.controllers.v1.auth import auth
from app.controllers.v1.test import test

app.register_blueprint(default.MOD)
app.register_blueprint(auth.MOD)
app.register_blueprint(test.MOD)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    if request.method == 'DELETE':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)
