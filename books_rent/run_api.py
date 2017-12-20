# coding: utf-8

from books_rent import app, db, api
from books_rent.resources.book import Book


def route_resources():
    api.add_resource(Book, '/book')


def run_api():
    db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    route_resources()
    run_api()
