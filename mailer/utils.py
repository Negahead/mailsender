from datetime import datetime
import re
import calendar

domain = "sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org"
auth_key = "key-9f939581473944b38338d87cdb47c14"


def parse_date(year, month, day, hour=0, minute=0, second=0, tz='+0800'):
    try:
        date = datetime(year, month, day, hour, minute, second)
        tz_info = re.compile("\+\d{4}")
        if not re.search(tz_info, tz):
            raise ValueError("time zone format {0} must be like (+|-)\d\d\d\d".format(tz))
        return date.strftime('%a, %d %b %Y %H:%M:%S ' + tz)
    except ValueError:
        raise ValueError


def to_utc_timestamp(year, month, day, hour=0, minute=0, second=0):
    try:
        c = calendar.timegm((year, month, day, hour, minute, second))
        return c-8*3600
    except (SyntaxError, ValueError, TypeError):
        return None


def from_utf_timestamp(timestamp):
    s = datetime.utcfromtimestamp(timestamp+8*3600)
    return s.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print(to_utc_timestamp(2018, 4, 18, 15, 57, 37))
    print(from_utf_timestamp(1524038257.243292))

