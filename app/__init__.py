from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import config as Config
from .resources.helloworld import HelloWorld 
import os

# basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()
api = Api()

def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app.config.from_object(Config[config_name])

    Config[config_name].init_app(app)
    
    # Set up extensions
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    return app

api.add_resource(HelloWorld, '/')
# api.add_resource(UserResource, '/user')