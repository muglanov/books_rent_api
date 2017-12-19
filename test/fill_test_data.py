# coding: utf-8

from sqlalchemy import *

engine = create_engine('postgresql://postgres:12345678@localhost/books_rent')
metadata = MetaData()

user = Table('user', metadata,
    Column('user', Integer, primary_key=True),
    Column('username', String(), nullable=False, unique=True),
    Column('password', String(), nullable=False),
    Column('salt', String(), nullable=False),
    Column('money', Integer, nullable=False)
)

book = Table('book', metadata,
    Column('book', Integer, primary_key=True),
    Column('author', String(), nullable=False),
    Column('name', String(), nullable=False, unique=True),
    Column('rent_price', Integer, nullable=False)
)

rent = Table('rent', metadata,
    Column('rent', Integer, primary_key=True),
    Column('user', Integer, ForeignKey('user.user'), nullable=False),
    Column('book', Integer, ForeignKey('book.book'), nullable=False),
    Column('dt', Date, nullable=False),
    Column('rental_dt', Date, nullable=False)
)

metadata.create_all(engine)