from datetime import datetime
import re


def parse_date(year, month, day, hour=0, minute=0, second=0, tz='+0800'):
    try:
        date = datetime(year, month, day, hour, minute, second)
        tz_info = re.compile("\+\d{4}")
        if not re.search(tz_info, tz):
            raise ValueError("time zone format {0} must be like (+|-)\d\d\d\d".format(tz))
        return date.strftime('%a, %d %b %Y %H:%M:%S ' + tz)
    except ValueError:
        raise ValueError

