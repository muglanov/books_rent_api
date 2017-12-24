# coding: utf-8

from json import loads
from datetime import date, timedelta

from flask_restful import Resource, request

from books_rent import db
from books_rent.models import Rent as RentModel, Book as BookModel, User as UserModel


class Rent(Resource):

    def get(self):
        if not request.data:
            return {'status': False, 'error': 'Not request data'}
        username = loads(request.data).get('username')
        token = request.headers.get('token')
        if username is None or token is None:
            return {'status': False, 'error': 'Username or token is none'}
        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {'status': False, 'error': 'No user with username'}
        if user.token is None or user.token != token:
            return {'status': False, 'error': 'User is not authorized or session is outdated'}
        user_rents = RentModel.query.filter_by(user=user.user).all()
        result = []
        for user_rent in user_rents:
            if user_rent.rental_end_dt <= date.today():
                db.session.delete(user_rent)
            else:
                result.append({
                    'name': user_rent.book_row.name,
                    'author': user_rent.book_row.author,
                    'rental_end_dt': user_rent.rental_end_dt.isoformat()
                })
        return {'status': True, 'error': None, 'rented_books_list': result}

    def post(self):
        if not request.data:
            return {'status': False, 'error': 'Not request data'}
        data = loads(request.data)
        username = data.get('username')
        book_id = data.get('book_id')
        month_count = data.get('month_count')
        token = request.headers.get('token')
        if username is None or token is None:
            return {'status': False, 'error': 'Username or token is none'}
        if book_id is None:
            return {'status': False, 'error': 'Book id is none'}
        if month_count is None:
            return {'status': False, 'error': 'Month count is none'}
        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {'status': False, 'error': 'No user with username'}
        if user.token is None or user.token != token:
            return {'status': False, 'error': 'User is not authorized or session is outdated'}
        book = BookModel.query.filter_by(book=book_id).first()
        if book is None:
            return {'status': False, 'error': 'No book with book_id'}
        total_rent_cost = book.rent_price * month_count
        if total_rent_cost > user.money:
            return {'status': False, 'error': 'Not enough money'}
        total_days = month_count * 30
        rental_end_dt = date.today() + timedelta(days=total_days)
        new_rent = RentModel(user=user.user, book=book_id, rental_end_dt=rental_end_dt)
        db.session.add(new_rent)
        user.money = user.money - total_rent_cost
        try:
            db.session.commit()
        except Exception as e:
            return {'status': False, 'error': str(e)}
        return {'status': True, 'error': None}


