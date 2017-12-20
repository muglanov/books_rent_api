# coding: utf-8

from unittest import TestCase
from requests import get
from json import dumps, loads

from books_rent import app
from books_rent.run_api import route_resources


class TestFlaskApi(TestCase):

    def setUp(self):
        route_resources()
        self.web_api = app.test_client()

    def test_get_books(self):
        books =[
            # {'book': 1, 'author': 'Джоан Роулинг', 'name': 'Гари Поттер и философский камень', 'rent_price': 150},
            {'book': 2, 'author': 'Стивен Кинг', 'name': 'Оно', 'rent_price': 130},
            # {'book': 3, 'author': 'Рэй Брэдбери', 'name': '451 градус по Фаренгейту', 'rent_price': 50},
            # {'book': 4, 'author': 'Анджей Сапковский', 'name': 'Ведьмак', 'rent_price': 320},
            # {'book': 5, 'author': 'Зак Горман', 'name': 'Рик и Морти', 'rent_price': 400},
            # {'book': 6, 'author': 'Грег Гурвиц', 'name': 'Бэтмен. Тёмный Рыцарь.', 'rent_price': 85},
            # {'book': 7, 'author': 'Нил Гейман', 'name': 'Скандинавские боги', 'rent_price': 210},
            # {'book': 8, 'author': 'Лю Цысинь', 'name': 'Задача трёх тел', 'rent_price': 270},
            # {'book': 9, 'author': 'Ли Бардуго', 'name': 'Продажное королевство', 'rent_price': 25},
            # {'book': 10, 'author': 'Филип Пулман', 'name': 'Северное сияние', 'rent_price': 100},
            # {'book': 11, 'author': 'Дмитрий Глуховский', 'name': 'Метро 2033', 'rent_price': 190},
            # {'book': 12, 'author': 'Стивен Кинг', 'name': 'Сияние', 'rent_price': 200},
            # {'book': 13, 'author': 'Хадзимэ Исаяма', 'name': 'Атака на титанов', 'rent_price': 150},
            # {'book': 14, 'author': 'Бернард Вербер', 'name': 'Империя ангелов', 'rent_price': 170},
            # {'book': 15, 'author': 'Стивен Кинг', 'name': 'Зелёная миля', 'rent_price': 75},
            # {'book': 16, 'author': 'Джон Рональд Руэл Толкин', 'name': 'Властелин Колец', 'rent_price': 430},
            # {'book': 17, 'author': 'Эрих Мария Ремарк', 'name': 'Три товарища', 'rent_price': 180},
            # {'book': 18, 'author': 'Эрих Мария Ремарк', 'name': 'На западном фронте без перемен', 'rent_price': 150}
        ]
        app.test_request_context()
        response = self.web_api.get('/book')
        self.assertEqual(loads(response.data.decode()), books)
