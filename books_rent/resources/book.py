# coding: utf-8

from json import loads

from flask_restful import Resource, request

from books_rent.models import Book as BookModel, User as UserModel


class Book(Resource):

    def get(self):
        username = loads(request.data).get('username')
        token = request.headers.get('token')
        if username is None:
            return {'status': False, 'error': 'Username is none'}
        if token is None:
            return {'status': False, 'error': 'Token is none'}
        user = UserModel.query.filter_by(username=username).first()
        if user.token is None or user.token != token:
            return {'status': False, 'error': 'User is not authorized or session is outdated'}
        books = BookModel.query.all()
        result = []
        for book in books:
            result.append({
                'book': book.book,
                'author': book.author,
                'name': book.name,
                'rent_price': book.rent_price
            })
        return {'status': True, 'error': None, 'books_list': result}
