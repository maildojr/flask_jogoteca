import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{user}:{password}@{server}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        user = 'root',
        password = '',
        server = '127.0.0.1',
        database = 'jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'