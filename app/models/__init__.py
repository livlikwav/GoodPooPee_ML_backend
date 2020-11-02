# """
# These imports enable us to make all defined models members of the models module
# (as opposed to just thier python files)
# """
# Dependancy of order
from .user import User
from .pet import Pet
from .ppcam import Ppcam
from .ppsnack import Ppsnack
from .pad import Pad
from .pet_record import PetRecord
from .dailystatistics import DailyStatistics
from .monthlystatistics import MonthlyStatistics
# No dependancy
from .ppcam_serial_nums import PpcamSerialNums
from .ppsnack_serial_nums import PpsnackSerialNums
from .blacklist_user_token import BlacklistUserToken
from .blacklist_device_token import BlacklistDeviceToken

# ======= To avoid circular import error
# Dont import each model in manage.py
# Just use this init.py