import datetime
from dateutil.parser import parse

def datetime_to_string(dt: datetime.datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def date_to_string(date: datetime.date) -> str:
    return date.strftime('%Y-%m-%d')

def string_to_datetime(dt_str: str) -> datetime.datetime:
    dt = parse(dt_str)
    return dt

def string_to_date(dt_str: str) -> datetime.date:
    dt = parse(dt_str)
    return dt.date()