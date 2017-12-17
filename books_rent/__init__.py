# coding: utf-8
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from books_rent.utils import get_postgresql_db_uri

username = "postgres"
pwd = "12345678"
db_name = 'books_rent'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_postgresql_db_uri(username, pwd, db_name)
db = SQLAlchemy(app)
api = Api(app)

from books_rent.resources.book import Book

db.create_all()
api.add_resource(Book, '/book')

def main():
    app.run(debug=True)