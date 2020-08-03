# from .helloworld import HelloWorld
# from .user import UserApi, RegisterApi

def init_routes(api):
    from .helloworld import HelloWorld
    from .user import UserApi, RegisterApi

    api.add_resource(HelloWorld, '/')
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(UserApi, '/user/<int:user_id>')