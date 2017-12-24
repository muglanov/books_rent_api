# coding: utf-8

from unittest import TestCase, main
from json import loads, dumps
from random import randint

from books_rent import app, db
from books_rent.run_api import route_resources
from books_rent.test.test_data import test_books, test_users, fill_test_data


class TestFlaskApi(TestCase):

    @classmethod
    def setUpClass(cls):
        route_resources()
        db.create_all()
        fill_test_data()

    def setUp(self):
        self.web_api = app.test_client()

    def test_authorizing(self):
        for user in test_users:
            # авторизация пользователя
            data = dumps(dict(username=user['username'], password=user['password']))
            response = self.web_api.post('/sign-in', data=data, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

            # выход пользователя
            data = dumps({'username': user['username']})
            header = {'token': resp_content['token']}
            response = self.web_api.delete('/sign-out', data=data, content_type='plain-text/json', headers=header)
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

    def test_authorizing_with_wrong_data(self):
        # авторизация без данных
        response = self.web_api.post('/sign-in', content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # авторизация с пустыми данными
        data = dumps({})
        response = self.web_api.post('/sign-in', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # авторизация с неправильным пользователем
        data = dumps(dict(username='sample_user', password='sample_password'))
        response = self.web_api.post('/sign-in', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # авторизация с неправильным паролем
        data = dumps(dict(username='mavrik', password='sample_password'))
        response = self.web_api.post('/sign-in', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # выход пользователя без данных
        response = self.web_api.delete('/sign-out', content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # выход пользователя с пустыми данными
        data = dumps({})
        response = self.web_api.delete('/sign-out', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # выход пользователя с неправильным токеном
        data = dumps({'username': 'mavrik'})
        header = {'token': 'sample_token'}
        response = self.web_api.delete('/sign-out', data=data, content_type='plain-text/json', headers=header)
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

    def test_books(self):
        # авторизация пользователя
        user = test_users[0]
        data = dumps(user)
        response = self.web_api.post('/sign-in', data=data)
        resp_content = loads(response.data.decode())
        self.assertTrue(resp_content['status'])

        # запрос списка с валидным токеном
        user['token'] = resp_content['token']
        data = dumps({'username': user['username']})
        header = {'token': user['token']}
        response = self.web_api.get('/book', data=data, headers=header, content_type='plain-text/json')
        books = loads(response.data.decode())['books_list']
        self.assertEqual(len(books), len(test_books))
        for book in books:
            del book['book']
        for book in test_books:
            self.assertTrue(book in books)

        # выход пользователя
        data = dumps({'username': user['username']})
        response = self.web_api.delete('/sign-out', data=data, headers=header, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertTrue(resp_content['status'])

    def test_books_with_wrong_data(self):
        # получить список книг без данных
        response = self.web_api.get('/book', content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с пустыми данными
        data = dumps({})
        response = self.web_api.get('/book', data=data, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с неправильным пользователем
        data = dumps({'username': 'sample user'})
        header = {'token': 'sample token'}
        response = self.web_api.get('/book', data=data, headers=header, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с неправильным токеном
        data = dumps({'username': 'mavrik'})
        header = {'token': 'sample token'}
        response = self.web_api.get('/book', data=data, headers=header, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

    def test_rent(self):
        for i in range(len(test_users)):
            # авторизация пользователя
            user = test_users[i]
            data = dumps(user)
            response = self.web_api.post('/sign-in', data=data, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

            # запрос списка с валидным токеном
            user['token'] = resp_content['token']
            data = dumps({'username': user['username']})
            header = {'token': user['token']}
            response = self.web_api.get('/book', data=data, headers=header, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])
            books = resp_content.get('books_list')
            self.assertEqual(len(books), len(test_books))

            # добавление аренды
            book = books[randint(0, len(books) - 1)]
            data = dumps(dict(username=user['username'], book_id=book['book'], month_count=randint(1, 3)))
            response = self.web_api.post('/rent', data=data, headers=header,content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

            # недостаток денег на счету пользователя
            data = dumps(dict(username=user['username'], book_id=book['book'], month_count=100))
            response = self.web_api.post('/rent', data=data, headers=header, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertFalse(resp_content['status'])

            # дублирование аренды
            response = self.web_api.post('/rent', data=data, headers=header, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertFalse(resp_content['status'])

            # список арендованых пользователем книжек
            data = dumps({'username': user['username']})
            response = self.web_api.get('/rent', data=data, headers=header, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

            # выход пользователя
            response = self.web_api.delete('/sign-out', data=data, headers=header, content_type='plain-text/json')
            resp_content = loads(response.data.decode())
            self.assertTrue(resp_content['status'])

    def test_rent_with_wrong_data(self):
        # список аренды пользователя без данных
        response = self.web_api.get('/rent', content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с пустыми данными
        data = dumps({})
        response = self.web_api.get('/rent', data=data, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с неправильным пользователем
        data = dumps({'username': 'sample user'})
        header = {'token': 'sample token'}
        response = self.web_api.get('/rent', data=data, headers=header, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # с неправильным токеном
        data = dumps({'username': 'mavrik'})
        header = {'token': 'sample token'}
        response = self.web_api.get('/rent', data=data, headers=header, content_type='plain-text/json')
        status = loads(response.data.decode())['status']
        self.assertFalse(status)

        # аренда без данных
        response = self.web_api.post('/rent', content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # аренда с пустыми данными
        data = dumps({})
        response = self.web_api.post('/rent', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # аренда с неправильным пользователем
        data = dumps(dict(username='sample_user', password='sample_password'))
        response = self.web_api.post('/rent', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])

        # аренда с неправильныйм id книги
        data = dumps(dict(username='sample_user', book_id='-1'))
        response = self.web_api.post('/rent', data=data, content_type='plain-text/json')
        resp_content = loads(response.data.decode())
        self.assertFalse(resp_content['status'])


if __name__ == '__main__':
    main()