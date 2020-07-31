from flask_restful import Resource
from flask import jsonify

class HelloWorld(Resource):
    def get(self):
        return jsonify(msg = 'Hello, world')
