# coding: utf-8

from books_rent import app, db, api
from books_rent.resources.book import Book


if __name__ == '__main__':
    db.create_all()
    api.add_resource(Book, '/book')
    app.run(debug=True)
