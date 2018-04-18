try:
    import requests
except ImportError:
    raise ImportError("request module import failed,please install requests first")


from datetime import datetime
import calendar
import re
import os


option_list = ['o:tag', 'o:dkim', 'o:deliverytime', 'o:testmode', 'o:tracking', 'o:tracking-clicks',
               'o:tracking-opens', 'o:require-tls', 'o:skip-verification']


class MailSender:
    def __init__(self, domain, auth_key, mail_from=None, mail_to=None, cc=None, bcc=None, subject=None, text=None, html=None, **kwargs):
        self.domain = domain or ''
        self.auth_key = auth_key or ''
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.text = text
        self.html = html
        self.attachment = []
        self.option_dict = {}

    def __setitem__(self, key, value):
        self.option_dict[key] = value

    def __getitem__(self, item):  # can only set options
        try:
            return self.option_dict[item]
        except KeyError:
            try:
                return self.__getattribute__(item)
            except AttributeError:
                return None

    @staticmethod
    def to_utc_timestamp(year, month, day, hour=0, minute=0, second=0):
        try:
            c = calendar.timegm((year, month, day, hour, minute, second))
            return c-8*3600
        except (SyntaxError, ValueError, TypeError):
            return None

    @staticmethod
    def from_utf_timestamp(timestamp):
        s = datetime.utcfromtimestamp(timestamp+8*3600)
        return s.strftime('%Y-%m-%d %H:%M:%S')

    def set_delivery_time(self, year, month, day, hour, minute, second, tz):
        try:
            date = datetime(year, month, day, hour, minute, second)
            tz_info = re.compile("\+\d{4}")
            if re.search(tz_info, tz):
                self.option_dict['o:deliverytime'] = date.strftime('%a, %d %b %Y %H:%M:%S ' + tz)
            else:
                raise ValueError("time zone format {0} must be like (+|-)\d\d\d\d".format(tz))
        except ValueError:
            raise ValueError

    def add_attachment(self, attachment_file_name):
        try:
            fh = open(attachment_file_name, "rb")
            file_name = os.path.basename(fh.name)
            attach_tuple = tuple(["attachment", tuple([file_name, fh.read()])])
            self.attachment.append(attach_tuple)
        except FileNotFoundError:
            print("{0} not found")
            pass

    def generate_form_data(self):
        form_data = dict()
        form_data['from'] = self.mail_from or ''
        form_data['to'] = self.mail_to or ''
        form_data['subject'] = self.subject or ''
        if self.text is not None and self.html is not None:
            form_data['html'] = self.html  # use html primarily
        if self.text is not None:
            form_data['text'] = self.text
        if self.html is not None:
            form_data['html'] = self.html
        return form_data

    def send_email(self):
        try:
            form_data = self.generate_form_data()
            form_data.update(self.option_dict)
            post = requests.post(
                "https://api.mailgun.net/v3/"+self.domain+"/messages",
                auth=("api", self.auth_key),
                files=self.attachment,
                data=form_data)
            if post.status_code == 200:
                print("successfully send mail to {0}".format(self.mail_to))
            else:
                try:
                    print("send mail failed: " + post.json()['message'])
                except KeyError:
                    pass
        except Exception:
            pass
        finally:
            print("successfully processed send {0} job!".format(self.mail_to))

    def set_receiver(self, receiver):
        """
        receiver is a file-like object or a string,or even an iterable
        :param receiver: 
        :return: 
        """
        if hasattr(receiver, 'read'):
            try:
                for mail_to in receiver.readlines():
                    self.mail_to = mail_to.strip()
                    self.send_email()
            except (FileNotFoundError, IOError, OSError):
                pass
        if isinstance(receiver, (str, list)):
            self.mail_to = receiver

    def set_html_content(self, html_content):
        """
        :param html_content: a file path or a literal string
        :return: 
        """
        if hasattr(html_content, 'read'): # read in 'rb' mode
            fh = html_content
            self.html = fh.read()
        else:
            try:
                fh = open(html_content, "rb", encoding="UTF-8")
                self.html = fh.read()
            except (FileNotFoundError, TypeError, ValueError, IOError):
                if isinstance(html_content, str):
                    self.html = html_content
                else:
                    raise ValueError("{0} is not a valid file path or a literal str")

    def set_subject(self, subject):
        if not isinstance(subject, str):
            raise ValueError("{0} is not of type str".format(subject))
        self.subject = subject


if __name__ == '__main__':
    # m = MailSender(
    #     domain='sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org',
    #     auth_key='key-9f939581473944b38338d87cdb47c147',
    #     mail_from="buyInt <postmaster@sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgub.org>")
    m=MailSender(domain='mergerhunt.com', auth_key='key-d7e1699d16d39be46f3478cba69375d9',
                 mail_from='mailgun@mergerhunt.com')
    m.set_receiver("zhangxiangqi@mergersmatch.com")
    # m.set_subject("sssssssssssssssssssssssssssubject")
    # m.set_html_content(open("C:\\Users\\zhangxiangqi\\Desktop\\gongshang\\html.txt", "rb"))
    m.set_html_content("""{"client-info": {}, "event": "delivered", "geolocation": {}, "ip": "", "recipient": "1097503158@qq.com", "recipient-domain": "qq.com", "timestamp": "2018-04-18 15:08:58", "tags": ["tag"]}
""")
    m['o:tag'] = ["tag1111111111111111"]
    m['o:tracking-opens'] = True
    m['o:tracking-clicks'] = True
    m.send_email()














