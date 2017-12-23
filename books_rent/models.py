from books_rent import db


class User(db.Model):
    __tablename__ = 'user'

    user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    salt = db.Column(db.String(), nullable=False)
    token = db.Column(db.String())
    money = db.Column(db.Integer, nullable=False)


class Book(db.Model):
    __tablename__ = 'book'

    book = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    rent_price = db.Column(db.Integer, nullable=False)


class Rent(db.Model):
    __tablename__ = 'rent'
    __table_args__ = (db.UniqueConstraint('user', 'book', name='_user_book_uc'),)

    rent = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.user'), nullable=False)
    book = db.Column(db.Integer, db.ForeignKey('book.book'), nullable=False)
    rental_end_dt = db.Column(db.Date, nullable=False)

    user_row = db.relation(User)
    book_row = db.relation(Book)