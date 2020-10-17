from flask_restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {
            "msg" : "Hello, world"
        }, 200
