#!/usr/bin/env python
# -*- coding: utf-8 -*-

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import app, db, cache
import datetime


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer)
    email = db.Column(db.String(), index=True, primary_key=True)
    password_hash = db.Column(db.String())
    token = db.Column(db.String(), index=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    account_type = db.Column(db.Integer())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=app.config['TOKEN_MAX_AGE'],):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        self.token = s.dumps({'id': self.id})
        db.session.commit()
        return self.token

    @property
    def account_type_string(self):
        if self.account_type == 0:
            return 'Student'
        if self.account_type == 1:
            return 'Faculty'
        if self.account_type == 2:
            return 'Admin'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'token': self.token,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'account_type': self.account_type_string
        }

    @staticmethod
    @cache.memoize(app.config["CACHE_TIMEOUT"])
    def data_by_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return data

    @staticmethod
    def verify_auth_token(token):
        user_data = User.data_by_token(token)
        if user_data is None:
            return None
        user = db.session.query(User).filter(
            User.id == user_data['id']).first()
        if not user or user.token != token:
            return None
        return user
