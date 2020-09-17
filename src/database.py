import os
from flask_pymongo import PyMongo
from src.secrets import get_secret

# mockable PyMongo instance
mongo = PyMongo()

def get_connection_string():
    username = os.environ.get('MONGO_USERNAME')
    password = get_secret(os.environ.get('MONGO_PASSWORD_SECRET_KEY')) if username else ''
    auth = '{username}:{password}@'.format(username=username, password=password) if username else ''
    host = os.environ.get('MONGO_HOST')
    database = os.environ.get('MONGO_DATABASE')
    options = '?authSource=admin' if username else ''

    return 'mongodb://{auth}{host}/{database}{options}'.format(
        auth=auth,
        host=host,
        database=database,
        options=options
    )
