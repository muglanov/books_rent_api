# coding: utf-8

from unittest import TestCase, main
from json import loads, dumps
from random import randint

from books_rent import app
from books_rent.run_api import route_resources
from books_rent.test.test_data import test_books, test_users, fill_test_data


class TestFlaskApi(TestCase):

    @classmethod
    def setUpClass(cls):
        route_resources()
        fill_test_data()

    def setUp(self):
        self.web_api = app.test_client()

    def test_authorizing(self):
        for user in test_users:
            data = dict(username=user['username'], password=user['password'])
            response = self.web_api.get('/signin', query_string=data)
            resp_content = loads(response.data.decode())
            # self.assertEqual(resp_content['status'], True)
            self.assertTrue(resp_content['status'], 'Sign in status')
            response = self.web_api.get('/signout', query_string=dict(username=user['username'], token=resp_content['token']))
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'], 'Sign out status')

    def test_get_books(self):
        data = {'username': 'mavrik', 'password': 'qwerty12345'}
        response = self.web_api.post('/signin', query_string=data)
        resp_content = loads(response.data.decode())
        token = resp_content['token']
        data = {'username': 'mavrik', 'token': token}
        response = self.web_api.get('/book', query_string=data)
        books = loads(response.data.decode())['books_list']
        self.assertEqual(len(books), len(test_books))