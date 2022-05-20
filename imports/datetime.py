from datetime import datetime, timedelta

def datetime_to_int(datetime_obj):
    diff = datetime_obj - datetime.min
    return diff.days * 24 * 60 * 60 + diff.seconds

def int_to_datetime(int):
    return datetime.min + timedelta(0, int)


def get_now():
    return datetime_to_int(datetime.now()) # if seconds change to ms
