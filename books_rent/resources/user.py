# coding: utf-8

from flask_restful import Resource, request

from books_rent import authorized_users
from books_rent.models import User as UserModel
from books_rent.utils import unique_token


class UserSignIn(Resource):

    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')
        if username is None or password is None:
            return {'status': False, 'error': 'Username or password is none'}, 401
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'status': False, 'error': 'User with this username'}, 401
        salt = user.salt
        salted_pwd = '{}{}'.format(salt, password)
        if salted_pwd != user.password:
            return {'status': False, 'error': 'User with this username and password not exist'}, 401
        token = unique_token()
        authorized_users[token] = user
        return {'status': True, 'token': token, 'error': None}


class UserSignOut(Resource):

    def get(self):
        token = request.args.get('token')
        if token and authorized_users.get(token):
            del authorized_users[token]
        return {'status': True, 'error': None}