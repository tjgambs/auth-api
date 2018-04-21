#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app.models.user import User
from app import app, db, auth, basicauth


MOD = Blueprint("v1_auth", __name__, url_prefix="/v1/auth")


@MOD.route('/user', methods=['POST'])
def new_user():
    if request.method == 'OPTIONS':
        return None
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    account_type = request.json.get('accountType')
    if (email is None or password is None
            or first_name is None or last_name is None
            or account_type is None):
        abort(400)
    if User.query.filter_by(email=email).first() is not None:
        abort(400, 'Email already in use.')
    user = User(email=email, first_name=first_name, last_name=last_name, account_type=account_type)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    user.generate_auth_token(app.config['TOKEN_MAX_AGE'])
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=user.serialize
        )
    )

@MOD.route('/update_user', methods=['POST'])
@auth.login_required
def update_user():
    if request.method == 'OPTIONS':
        return None
    
    email = request.json.get('email')
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    if email is None or first_name is None or last_name is None:
        abort(400)

    g.user.email = email
    g.user.first_name = first_name
    g.user.last_name = last_name
    db.session.commit()

    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=g.user.serialize
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


@MOD.route("/user/verify", methods=["GET"])
@auth.login_required
def verify():
    return jsonify(
        prepare_json_response(
            message=None,
            success=True
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
