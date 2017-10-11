#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, g
from app.controllers.v1.auth.auth import auth
from app.utils import prepare_json_response


MOD = Blueprint("v1_test", __name__, url_prefix="/v1/test")

@MOD.route('/', methods = ['GET'])
@auth.login_required
def new_user():
    return jsonify(
        prepare_json_response(
            data='Hello, %s!' % g.user.email,
            message="OK",
            success=True
        )
    ) 