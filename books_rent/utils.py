# coding: utf-8

POSTGRES = 'postgresql'


def get_postgresql_db_uri(user, password, db_name, host='localhost'):
    return '{}://{}:{}@{}/{}'.format(POSTGRES, user, password, host, db_name)