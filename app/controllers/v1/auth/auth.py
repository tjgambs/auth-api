#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app.models.user import User
from app import app, db, auth, basicauth


MOD = Blueprint("v1_auth", __name__, url_prefix="/v1/auth")


@MOD.route('/user', methods = ['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400)
    if User.query.filter_by(email=email).first() is not None:
        abort(400, 'Email already in use.')
    user = User(email = email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=user.serialize
        )
    ) 

@MOD.route("/user/token", methods=["GET"])
@basicauth.login_required
def token():
    token = g.user.generate_auth_token(app.config['TOKEN_MAX_AGE'])
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data=g.user.serialize
        )
    )

@basicauth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(401, 'The email you have entered is invalid.')
    if not user.verify_password(password):
        abort(401, 'The password you have entered is invalid.')
    g.user = user
    return True

@auth.verify_token
def verify_token(token):
    g.user = User.verify_auth_token(token)
    if not g.user:
        abort(401, 'Invalid User')
    elif g.user.token != token:
        abort(423, 'Your account has been automatically logged out due to activity on another device.')
    return True







