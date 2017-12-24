# coding: utf-8

from hashlib import sha1
from json import loads

from flask_restful import Resource, request

from books_rent import db
from books_rent.models import User as UserModel
from books_rent.utils import unique_token


class UserSignIn(Resource):

    def post(self):
        if not request.data:
            return {'status': False, 'error': 'Not request data'}, 401
        data = loads(request.data)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return {'status': False, 'error': 'Username or password is none'}, 401
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'status': False, 'error': 'User or password is wrong'}, 401
        salt = user.salt
        prepeared_pwd = '{}{}'.format(salt, password)
        salted_pwd = sha1(prepeared_pwd.encode()).hexdigest()
        if salted_pwd != user.password:
            return {'status': False, 'error': 'User or password is wrong'}, 401
        token = unique_token()
        user.token = token
        db.session.commit()
        return {'status': True, 'token': token, 'error': None}


class UserSignOut(Resource):

    def delete(self):
        if not request.data:
            return {'status': False, 'error': 'Not request data'}
        username = loads(request.data).get('username')
        token = request.headers.get('token')
        if username is None or token is None:
            return {'status': False, 'error': 'Username or token is none'}
        user = UserModel.query.filter_by(username=username).first()
        if user.token is None or user.token != token:
            return {'status': False, 'error': 'User is not authorized or session is outdated'}
        user.token = None
        db.session.commit()
        return {'status': True, 'error': None}