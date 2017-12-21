# coding: utf-8

import psycopg2
from hashlib import sha1
from random import random

test_books = [
    {'author': 'Джоан Роулинг', 'name': 'Гари Поттер и философский камень', 'rent_price': 150},
    {'author': 'Стивен Кинг', 'name': 'Оно', 'rent_price': 130},
    {'author': 'Рэй Брэдбери', 'name': '451 градус по Фаренгейту', 'rent_price': 50},
    {'author': 'Анджей Сапковский', 'name': 'Ведьмак', 'rent_price': 320},
    {'author': 'Зак Горман', 'name': 'Рик и Морти', 'rent_price': 400},
    {'author': 'Грег Гурвиц', 'name': 'Бэтмен. Тёмный Рыцарь.', 'rent_price': 85},
    {'author': 'Нил Гейман', 'name': 'Скандинавские боги', 'rent_price': 210},
    {'author': 'Лю Цысинь', 'name': 'Задача трёх тел', 'rent_price': 270},
    {'author': 'Ли Бардуго', 'name': 'Продажное королевство', 'rent_price': 25},
    {'author': 'Филип Пулман', 'name': 'Северное сияние', 'rent_price': 100},
    {'author': 'Дмитрий Глуховский', 'name': 'Метро 2033', 'rent_price': 190},
    {'author': 'Стивен Кинг', 'name': 'Сияние', 'rent_price': 200},
    {'author': 'Хадзимэ Исаяма', 'name': 'Атака на титанов', 'rent_price': 150},
    {'author': 'Бернард Вербер', 'name': 'Империя ангелов', 'rent_price': 170},
    {'author': 'Стивен Кинг', 'name': 'Зелёная миля', 'rent_price': 75},
    {'author': 'Джон Рональд Руэл Толкин', 'name': 'Властелин Колец', 'rent_price': 430},
    {'author': 'Эрих Мария Ремарк', 'name': 'Три товарища', 'rent_price': 180},
    {'author': 'Эрих Мария Ремарк', 'name': 'На западном фронте без перемен', 'rent_price': 150}
]

test_users = [
    {'username': 'mavrik', 'password': 'qwerty12345', 'money': 10000},
    {'username': 'capture', 'password': 'qazwsxedc', 'money': 1570},
    {'username': 'mumu', 'password': 'plmokn', 'money': 410},
    {'username': 'nikolay', 'password': 'zxc123asd', 'money': 3500},
    {'username': 'kazan', 'password': 'belykrolik123', 'money': 5333},
    {'username': 'logan123', 'password': 'superxmen123', 'money': 7000},
    {'username': 'argentinoff', 'password': 'yamaika50', 'money': 10000}
]


def insert_user_query(username, password, money):
    salt = sha1(str(random()).encode()).hexdigest()
    prepeared_pwd = '{}{}'.format(salt, password)
    salted_pwd = sha1(prepeared_pwd.encode()).hexdigest()
    return '''INSERT INTO public.user 
    (username, password, salt, money) VALUES 
    ('{}', '{}', '{}', {});
    '''.format(username, salted_pwd, salt, money)


def insert_book_query(name, author, rent_price):
    return '''INSERT INTO book 
        (author, name, rent_price) VALUES 
        ('{}', '{}', {});
        '''.format(author, name, rent_price)


def fill_test_data():
    with psycopg2.connect('dbname=books_rent user=postgres host=localhost password=12345678') as conn:
        cur = conn.cursor()

        # создание тестовых пользователей
        cur.execute('DELETE FROM public.user;')
        for user in test_users:
            cur.execute(insert_user_query(user['username'], user['password'], user['money']))

        # создание тестовых книг
        cur.execute('DELETE FROM public.book;')
        for book in test_books:
            cur.execute(insert_book_query(book['name'], book['author'], book['rent_price']))

