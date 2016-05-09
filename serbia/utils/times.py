# -*- coding: utf-8 -*-

import calendar
from datetime import datetime
from datetime import timedelta
from datetime import date

def to_timestamp(dt):
    if not dt:
        return dt
    return calendar.timegm(dt.utctimetuple())


def to_iso_datetime(ts):
    if not ts:
        return ts
    dt = datetime.utcfromtimestamp(ts)
    cn_dt = dt + timedelta(hours = 8)
    return cn_dt.strftime("%Y-%m-%d %H:%M:%S")


def to_iso_date(ts):
    dt = datetime.utcfromtimestamp(ts)
    cn_dt = dt + timedelta(hours = 8)
    return cn_dt.strftime("%Y-%m-%d")


def roundTime(dt=None, roundTo=60*60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 hour.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)


def add_months(source_date, months):
    # to cn ts
    source_date = source_date + timedelta(hours = 8)

    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12 )
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year,month)[1])
    return date(year, month, day)
