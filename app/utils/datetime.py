"""
Mysql with SQLAlchemy cant save timezone info
So, all db.Datetime be saved by datetime.datetime.utcnow
db.Date in DailyStatistics, MonthlyStatistics be saved by KST
"""
import datetime
import pytz
import sys
from dateutil.parser import parse

KST = pytz.timezone('Asia/Seoul')

def get_kst_date(naive_utc):
    """
    Change naive utc datetime to Date by KST
    :Param: datetime.datetime(tzinfo=None, but actually UTC)
    :Return: datetime.date(set by KST)
    """
    if(naive_utc.tzinfo is not None):
        raise TypeError('datetime arg is not naive datetime')
    else:
        utc_datetime = pytz.utc.localize(naive_utc)
        ktc_datetime = utc_datetime.astimezone(KST)
        ktc_date = ktc_datetime.date()
        return ktc_date

def get_kst_datetime(naive_utc):
    """
    Change naive utc datetime to KST.datetime
    :Param: datetime.datetime(tzinfo=None, but actually UTC)
    :Return: datetime.datetime(tzinfo='Asia/Seoul', and actually KST)
    """
    if(naive_utc.tzinfo is not None):
        raise TypeError('datetime arg is not naive datetime')
    else:
        utc_datetime = pytz.utc.localize(naive_utc)
        ktc_datetime = utc_datetime.astimezone(KST)
        return ktc_datetime

