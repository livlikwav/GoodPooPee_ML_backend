import datetime
import pytz

KST = pytz.timezone('Asia/Seoul')

def get_utc_now():
    """
    Get datetime.now() of UTC
    :Param:
    :Return: datetime.datetime(tzinfo=<UTC>)
    """
    now = datetime.datetime.utcnow()
    return pytz.utc.localize(now)

def utc_to_kst(utc_time):
    """
    Change UTC to KST datetime
    if param.tzinfo!=pytz.utc: raise TypeError
    :Param: datetime.datetime(tzinfo=<UTC>)
    :Return: datetime.datetime(tzinfo=<DstTzInfo 'Asia/Seoul' KST+9:00:00 STD>)
    """
    #check tzinfo
    if(utc_time.tzinfo == pytz.utc):
        return utc_time.astimezone(KST)
    else:
        raise TypeError