# coding: utf-8

import psycopg2
from hashlib import sha1
from random import random


def insert_user_query(username, password, money):
    salt = sha1(str(random()).encode()).hexdigest()
    prepeared_pwd = '{}{}'.format(salt, password)
    salted_pwd = sha1(prepeared_pwd.encode()).hexdigest()
    return '''INSERT INTO user 
    (username, password, salt, money) VALUES 
    ({}, {}, {}, {})
    '''.format(username, salted_pwd, salt, money)

def insert_book_query(name, author, rent_price):
    return '''INSERT INTO book 
        (author, name, rent_price) VALUES 
        ({}, {}, {}, {})
        '''.format(author, name, rent_price)

with psycopg2.connect('dbname="books_rent" user="postgres" host="localhost" password="12345678"') as conn:
    cur = conn.cursor()
    cur.execute(insert_user_query('Василий', '123456', 7500))
    cur.execute(insert_book_query('Гари Поттер и философский камень', 'Джоан Роулинг', 150))