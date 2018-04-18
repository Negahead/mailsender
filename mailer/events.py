import requests
import json
from datetime import datetime
import calendar
import os
import re
import sys

# from .utils import domain as mailgun_domain
# from .utils import auth_key as mailgun_auth_key


class Event:
    """
     mailgun tracks every event that happened to your emails and makes this data available through Event API
    """
    def __init__(self, domain, auth_key, **kwargs):
        self.domain = domain
        self.auth_key = auth_key
        self.begin_time = None
        self.end_time = None
        self.ascending = None
        self.limit = None
        self.recipient = None
        self.mail_event = None
        self.tags = None

    @staticmethod
    def to_utc_timestamp(year, month, day, hour=0, minute=0, second=0):
        try:
            c = calendar.timegm((year, month, day, hour, minute, second))
            return c-8*3600
        except (SyntaxError, ValueError, TypeError):
            return None

    @staticmethod
    def from_utf_timestamp(timestamp):
        try:
            s = datetime.utcfromtimestamp(timestamp+8*3600)
            return s.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            return None

    def set_begin_time(self, year, month, day, hour, minute, second):
        utc_begin_time = Event.to_utc_timestamp(year, month, day, hour, minute, second)
        if utc_begin_time is not None:
            self.begin_time = utc_begin_time

    def set_end_time(self, year, month, day, hour, minute, second):
        utc_end_time = Event.to_utc_timestamp(year, month, day, hour, minute, second)
        if utc_end_time is not None:
            self.end_time = utc_end_time

    def get_log(self, ascending=None, limit=10, recipient=None, mail_event=None, tags=None):
        """
        :param ascending:  yes or no
        :param limit: 
        :param recipient: 
        :param mail_event: accepted,rejected,delivered,failed,opened,clicked,unsubscribed,complained,stored
        :param tags: user-defined tag
        :return: 
        """
        payload = dict()
        if limit is not None and limit != 0:
            payload['limit'] = limit
        if recipient is not None:
            if isinstance(recipient, str):
                payload['recipient'] = recipient

        if mail_event is not None:
            if isinstance(mail_event, str):
                payload['event'] = mail_event

        if tags is not None:
            if isinstance(tags, str):
                payload['tags'] = '"' + tags + '"'

        if self.begin_time is not None:
            payload['begin'] = self.begin_time

        if self.end_time is not None:
            payload['end'] = self.end_time

        if ascending is not None and isinstance(ascending, str):
            payload['ascending'] = ascending

        get = requests.get("https://api.mailgun.net/v3/"+self.domain+"/events",
                           auth=("api", self.auth_key),
                           params=payload)
        if get.status_code == 200:
            # print(json.dumps(get.json(), indent=4, ensure_ascii=False))
            current_dir = os.path.abspath('.')
            file_name = str(int(datetime.now().timestamp()))+"_log.txt"
            file_path = current_dir + os.path.sep + file_name
            fh = None
            try:
                fh = open(file_path, 'w', encoding="UTF-8")
            except Exception:
                raise IOError("open file {0} failed".format(file_path))
            for j in get.json()['items']:
                value = {}
                # client-info
                if 'client-info' in j:
                    value['client-info'] = j['client-info'] or {}
                else:
                    value['client-info'] = {}
                # event: clicked,delivered...
                if 'event' in j:
                    value['event'] = j['event'] or ''
                else:
                    value['event'] = ''
                # country,region,city
                if 'geolocation' in j:
                    value['geolocation'] = j['geolocation'] or {}
                else:
                    value['geolocation'] = {}
                # ip address
                if 'ip' in j:
                    value['ip'] = j['ip'] or ''
                else:
                    value['ip'] = ''
                # recipient
                if 'recipient' in j:
                    value['recipient'] = j['recipient'] or ''
                else:
                    value['recipient'] = ''
                # recipient-domain,like qq.com, 163.com, google.com,...etc
                if 'recipient-domain' in j:
                    value['recipient-domain'] = j['recipient-domain'] or ''
                else:
                    value['recipient-domain'] = ''
                # timestamp
                if 'timestamp' in j:
                    # datetime.from
                    t = Event.from_utf_timestamp(j['timestamp'])
                    if t is not None:
                        value['timestamp'] = t
                else:
                    value['timestamp'] = ''
                # user-defined email tags, may be useful later
                if 'tags' in j:
                    value['tags'] = j['tags'] or []
                else:
                    value['tags'] = []
                json_string = json.dumps(value, ensure_ascii=False)
                fh.write(json_string)
                fh.write("\n")
            fh.close()
        else:
            print("error request log info")
            print(get.status_code)
            print(get.text)

    def stats(self, event_types, durations):
        if not isinstance(event_types, (str, list)):
            raise TypeError("event types {0} should be of string or list".format(event_types))
        if not isinstance(durations, str):
            raise TypeError("duration {0} should be of string type".format(durations))
        if not re.match("^[0-9]+[ymd]$", durations):
            raise ValueError("duration {0} should be like [0-9]+[ymd]".format(durations))
        g = requests.get(
            "https://api.mailgun.net/v3/"+self.domain+"/stats/total",
            auth=("api", self.auth_key),
            params={"event": event_types,
                    "duration": str(durations),
                    })
        if g.status_code == 200:
            current_dir = os.path.abspath('.')
            file_name = str(int(datetime.now().timestamp()))+"_stats.txt"
            file_path = current_dir + os.path.sep + file_name
            fh = None
            try:
                fh = open(file_path, 'w', encoding="UTF-8")
            except Exception:
                raise IOError("open file {0} failed".format(file_path))
            json_string = json.dumps(g.json(), ensure_ascii=False)
            fh.write(json_string)
            fh.write("\n")
            fh.close()
        else:
            print("error request stats info")
            print(g.status_code)
            print(g.text)

    def get_suppressions(self, suppression):
        """
        :param suppression:  bounces,unsubscribes,complaints
        :return: 
        """
        if not isinstance(suppression, str):
            raise TypeError("suppression {0} is a not str type".format(suppression))
        if suppression != 'bounces' and suppression != 'unsubscribes' and suppression != 'complaints':
            raise ValueError("suppresion {0} should be 'bounces' or 'unsubscribes', or 'complaints' ")
        g = requests.get(
            "https://api.mailgun.net/v3/"+self.domain+"/"+suppression,
            auth=("api", self.auth_key))
        if g.status_code == 200:
            current_dir = os.path.abspath('.')
            file_name = str(int(datetime.now().timestamp()))+"_"+suppression+".txt"
            file_path = current_dir + os.path.sep + file_name
            try:
                fh = open(file_path, 'w', encoding="UTF-8")
            except Exception:
                raise IOError("open file {0} failed".format(file_path))
            json_string = json.dumps(g.json(), ensure_ascii=False)
            fh.write(json_string)
            fh.write("\n")
            fh.close()
        else:
            print("error requesting suppresion info")
            print(g.status_code)
            print(g.text)


if __name__ == '__main__':
    e = ["accepted", "delivered", "failed", "opened", "clicked"]
    event = Event(domain='sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org',
                  auth_key='key-9f939581473944b38338d87cdb47c147')
    # event.stats(e, "2m")
    event.get_log(recipient='1097503158@qq.com')
    # event.get_suppressions('bounces')