# from .helloworld import HelloWorld
# from .user import UserApi, RegisterApi

def init_routes(api):
    from .helloworld import HelloWorld
    from .auth import RegisterApi, LoginApi, LogoutApi
    from .user import UserApi, UserPetApi
    from .pet import PetRegisterApi, PetApi
    from .ppcam import PpcamRegisterApi, PpcamApi

    # Helloworld
    api.add_resource(HelloWorld, '/')
    # Auth
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(LogoutApi, '/user/logout')
    # User
    api.add_resource(UserApi, '/user/<int:user_id>')
    api.add_resource(UserPetApi, '/user/<int:user_id>/pet')
    # Pet
    api.add_resource(PetRegisterApi, '/pet/register')
    api.add_resource(PetApi, '/pet/<int:pet_id>')
    # Ppcam
    api.add_resource(PpcamRegisterApi, '/ppcam/register')
    api.add_resource(PpcamApi, '/ppcam/<int:ppcam_id>')
