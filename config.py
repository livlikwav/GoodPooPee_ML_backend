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
    # SECRET_KEY = os.getnev('SECRET_KEY', 'ngle_api_tongchun')

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')

class TestConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')
                
class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = DB_URL
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'dev' : DevConfig,
    'test' : TestConfig,
    'production' : ProductionConfig,
    'default' : DevConfig
}