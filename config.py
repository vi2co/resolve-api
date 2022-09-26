from os import environ

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
DB_URI = environ.get('DB_URI')
TABLE_NAME = environ.get('TABLE_NAME')
NAMESERVER = environ.get('NAMESERVER')
