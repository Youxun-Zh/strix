"""
"""

import sys
import time

PY35 = sys.version_info >= (3, 5)


def format_timestamp(timestamp):
    """
    Weekday and month names for HTTP date/time formatting; always English!
    Return a string representation of a date according to RFC 1123 (HTTP/1.1).

    The supplied date must be in UTC.
    """
    _weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    _monthname = (None,  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    date_args = (_weekdayname[wd], day, _monthname[month], year, hh, mm, ss)
    http_date = "{}, {:02d} {} {} {:02d}:{:02d}:{:02d} GMT".format(*date_args)
    return http_date
