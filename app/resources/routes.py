# from .helloworld import HelloWorld
# from .user import UserApi, RegisterApi

def init_routes(api):
    from .helloworld import HelloWorld
    from .auth import RegisterApi, LoginApi, LogoutApi
    from .user import UserApi, UserPetApi, UserPpcamApi
    from .pet import PetRegisterApi, PetApi
    from .pet_record import PetRecordApi
    from .pet_record_image import PetRecordImageApi
    from .ppcam import PpcamRegisterApi, PpcamApi
    from .pad import PadApi
    from .ppsnack import PpsnackApi
    from .statistics import DailyStatApi, WeeklyStatApi, MonthlyStatApi, TotalMonthStatApi

    # Helloworld
    api.add_resource(HelloWorld, '/')
    # Auth
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(LogoutApi, '/user/logout')
    # User
    api.add_resource(UserApi, '/user/<int:user_id>')
    api.add_resource(UserPetApi, '/user/<int:user_id>/pets')
    api.add_resource(UserPpcamApi, '/user/<int:user_id>/ppcams')
    # Pet
    api.add_resource(PetRegisterApi, '/pet/register')
    api.add_resource(PetApi, '/pet/<int:pet_id>')
    # PetRecord
    api.add_resource(PetRecordApi, '/pet/<int:pet_id>/record')
    # PetRecordImage
    api.add_resource(PetRecordImageApi, '/pet/<int:pet_id>/record/image')
    # Ppcam
    api.add_resource(PpcamRegisterApi, '/ppcam/register')
    api.add_resource(PpcamApi, '/ppcam/<int:ppcam_id>')
    # Pad
    api.add_resource(PadApi, '/ppcam/<int:ppcam_id>/pad')
    # Ppsnack
    api.add_resource(PpsnackApi, '/ppcam/<int:ppcam_id>/ppsnack')
    # Statistics
    api.add_resource(DailyStatApi, '/pet/<int:pet_id>/report/daily')
    api.add_resource(WeeklyStatApi, '/pet/<int:pet_id>/report/weekly')
    api.add_resource(MonthlyStatApi, '/pet/<int:pet_id>/report/monthly')
    api.add_resource(TotalMonthStatApi, '/pet/<int:pet_id>/report/total')
    