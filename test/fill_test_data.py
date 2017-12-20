# coding: utf-8

import psycopg2
from hashlib import sha1
from random import random


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

with psycopg2.connect('dbname=books_rent user=postgres host=localhost password=12345678') as conn:
    cur = conn.cursor()

    # создание тестовых пользователей
    cur.execute('DELETE FROM public.user;')
    cur.execute(insert_user_query('mavrik', 'qwerty12345', 10000))
    cur.execute(insert_user_query('capture', 'qazwsxedc', 1570))
    cur.execute(insert_user_query('mumu', 'plmokn', 410))
    cur.execute(insert_user_query('nikolay', 'zxc123asd', 3500))
    cur.execute(insert_user_query('kazan', 'belykrolik123', 5333))
    cur.execute(insert_user_query('logan123', 'superxmen123', 7000))
    cur.execute(insert_user_query('argentinoff', 'yamaika50', 10000))

    # создание тестовых книг
    cur.execute('DELETE FROM public.book;')
    # cur.execute(insert_book_query('Гари Поттер и философский камень', 'Джоан Роулинг', 150))
    cur.execute(insert_book_query('Оно', 'Стивен Кинг', 130))
    # cur.execute(insert_book_query('451 градус по Фаренгейту', 'Рэй Брэдбери', 50))
    # cur.execute(insert_book_query('Ведьмак', 'Анджей Сапковский', 320))
    # cur.execute(insert_book_query('Рик и Морти', 'Зак Горман', 400))
    # cur.execute(insert_book_query('Бэтмен. Тёмный Рыцарь.', 'Грег Гурвиц', 85))
    # cur.execute(insert_book_query('Скандинавские боги', 'Нил Гейман', 210))
    # cur.execute(insert_book_query('Задача трёх тел', 'Лю Цысинь', 270))
    # cur.execute(insert_book_query('Продажное королевство', 'Ли Бардуго', 25))
    # cur.execute(insert_book_query('Северное сияние', 'Филип Пулман', 100))
    # cur.execute(insert_book_query('Метро 2033', 'Дмитрий Глуховский', 190))
    # cur.execute(insert_book_query('Сияние', 'Стивен Кинг', 200))
    # cur.execute(insert_book_query('Атака на титанов', 'Хадзимэ Исаяма', 150))
    # cur.execute(insert_book_query('Империя ангелов', 'Бернард Вербер', 170))
    # cur.execute(insert_book_query('Зелёная миля', 'Стивен Кинг', 75))
    # cur.execute(insert_book_query('Властелин Колец', 'Джон Рональд Руэл Толкин', 430))
    # cur.execute(insert_book_query('Три товарища', 'Эрих Мария Ремарк', 180))
    # cur.execute(insert_book_query('На западном фронте без перемен', 'Эрих Мария Ремарк', 150))

