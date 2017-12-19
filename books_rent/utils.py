# coding: utf-8

from hashlib import sha1
from random import random

POSTGRES = 'postgresql'


def get_postgresql_db_uri(user, password, db_name, host='localhost'):
    return '{}://{}:{}@{}/{}'.format(POSTGRES, user, password, host, db_name)


def unique_token():
    return sha1(str(random()).encode()).hexdigest()
