# coding: utf-8

from flask_restful import Resource

from books_rent.models import Book as BookModel


class Book(Resource):

    def get(self):
        books = BookModel.query.all()
        result = []
        for book in books:
            result.append({
                'book': book.book,
                'author': book.author,
                'name': 'Harry Potter',
                'rent_price': book.rent_price
            })
        return result
