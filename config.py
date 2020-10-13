import logging
import os

# DB Config
db = {
    'user' : 'myuser',
    'password' : '1q2w3e4r5t',
    'host' : 'mysql',
    'port' : 3306,
    'database' : 'gpp_db'
}

DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

class Config:
    DEBUG = False
    BUCKET_NAME = 'gpp-images-1'

    # JWT SECRET KEY
    if os.environ.get('JWT_SECRET_KEY'):
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    else:
        JWT_SECRET_KEY = 'JWT_SECRET_KEY_ENV_VAR_NOT_SET'
        print('JWT_SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    # flasgger config
    from swagger import swagger_config
    SWAGGER = swagger_config

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # logging config
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(pathname)s>%(message)s')

    @classmethod
    def init_app(cls, app):
        print('[Dev Config]THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')

class TestConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        print('[Test Config]THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')
                
class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = DB_URL
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # logging config
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(pathname)s>%(message)s')

config = {
    'dev' : DevConfig,
    'test' : TestConfig,
    'production' : ProductionConfig,
    'default' : DevConfig
}