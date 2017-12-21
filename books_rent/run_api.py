# coding: utf-8

from books_rent import app, db, api
from books_rent.resources.book import Book
from books_rent.resources.user import UserSignIn, UserSignOut


def route_resources():
    api.add_resource(Book, '/book')
    api.add_resource(UserSignIn, '/signin')
    api.add_resource(UserSignOut, '/signout')


def run_api():
    db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    route_resources()
    run_api()
