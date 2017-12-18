# coding: utf-8

from flask_restful import Resource, request

from books_rent import authorized_users
from books_rent.models import User as UserModel


class UserSignIn(Resource):

    def put(self):
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username, password=password).first()
        if user:
            token = 'token'
            authorized_users[user] = token
            return {'token': token}
        return {'token': None}, 401


class UserSignOut(Resource):

    def put(self):
        username = request.form['username']
        token = request.form['token']
        if authorized_users.get(username) and authorized_users[username] == token:
            del authorized_users[username]
        return {'result': 'ok'}