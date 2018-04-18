import json
import requests

from mailer import utils


def resend_simple_message():
    p =  requests.post(
        "https://se.api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/messages/STORAGE_URL",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
        data={"to": ["1097503158@qq.com"] })
    print(p.status_code)


def get_ip():
    g = requests.get(
        "https://api.mailgun.net/v3/ips",
        auth=("api", "key-9f939581473944b38338d87cdb47c147")
    )
    prettify_json(g.json())


def get_my_domain():
    g = requests.get(
        "https://api.mailgun.net/v3/domains",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
    )
    if g.status_code == 200:
        print("successfully fetched domain info:")
        prettify_json(g.json())


def send_will_message():
    p = requests.post(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/messages",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
        files=[("attachment", ("test.txt", open("C:\\Users\\zhangxiangqi\\Desktop\\gongshang\\url_void.txt","rb").read())),
               ("attachment", ("pic.jpg", open("C:\\Users\\zhangxiangqi\\Desktop\\gongshang\\pic.jpg","rb").read()))],
        data={
            "from": "postmaster@sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgub.org",
            "to": "will <1097503158@qq.com>",
            "subject": "Hello will",
            "text": "a, %my_var.name%",
            # "html":"<html>html version of the body</html>",
            "o:tag": ["message send use python API"],  # tag each outgoing message with a custom value
            "o:tracking-opens": True,
            "o:tracking-clicks": True,
            "o:my_var": {"name": "dopa", "age": 1}
        }
    )
    if p.status_code != 200:
        print("send mail failed")
        print(p.text)
    else:
        print("mail send")
        print(json.dumps(p.json(), indent=4))


def send_simple_message():
    json = [
        "zhouwei@mergersmatch.com" ,
        "zhangxiangqi@mergersmatch.com"
    ]
    p =  requests.post(
        "https://api.mailgun.net/v3/mergerhunt.com/messages",
        auth=("api", "key-d7e1699d16d39be46f3478cba69375d9"),
        files=[("attachment", ("test.txt", open("C:\\Users\\zhangxiangqi\\Desktop\\gongshang\\url_void.txt").read())),
               ("attachment",("pic.jpg", open("C:\\Users\\zhangxiangqi\\Desktop\\gongshang\\pic.jpg","rb").read()))],
        data={"subscribed":True,
              "from": "Excited User <excited@mergerhunt.com>",
              "to": ["zhouwei@mergersmatch.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!",
              "html": "<html>html version of the body</html>",
              "o:tag": ["message send use python API"],
              "o:tracking-opens": True,
              "o:tracking-clicks": True})
    if p.status_code == 200:
        print("mail send")
    else:
        print("send mail failed")
        print(p.text)


def prettify_json(json_obj):
    if not isinstance(json_obj,dict):
        raise TypeError("not a dict")
    print(json.dumps(json_obj, indent=4))


def get_credentials():
    print("fetching credentials......")
    g =  requests.get(
        "https://api.mailgun.net/v3/domains/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/credentials",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"))
    if g.status_code == 200:
        print("successfully fetched credential infos:")
        prettify_json(g.json())
    else:
        print("fetch credential infos failed")


def get_logs():
    print("requesting log history......")
    g =  requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/events",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
        params={
                "begin": "Tue, 17 April 2018 20:30:00 +0800",
                # "end": "Tue, 17 April 2018 21:59:00 +0800",
                "ascending":"yes",
                "limit":  20,
                "pretty": "yes",
                "event": "accepted OR delivered",
                "tags": '"message send use python API"',
                "recipient": "1097503158@qq.com"
        }) # accepted mail in this
    if g.status_code == 200:
        print("successfully queried log history,result is:")
        print(json.dumps(g.json(), indent=4))
    else:
        print("error requesting log history.")


def get_event():
    g = requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/events",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
        data={
            "begin": "Mon, 16 April 2018 09:00:00 +0800",
            "end": "Mon, 16 April 2018 17:00:00 +0800",
            "ascending": "yes",
            "event": "clicked"
        }
    )
    if g.status_code == 200:
        prettify_json(g.json())
    else:
        print("request events info failed")


def get_stats():
    g = requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/stats/total",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"),
        params={"event": ["accepted", "delivered", "failed"],
                "duration": "1m",
                })
    prettify_json(g.json())

def get_bounce():
    g = requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/bounces",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"))
    prettify_json(g.json())


def get_unsubscribes():
    g = requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/unsubscribes",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"))
    prettify_json(g.json())


def get_complaints():
    g = requests.get(
        "https://api.mailgun.net/v3/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/complaints",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"))
    prettify_json(g.json())


def get_webhooks():
    g =  requests.get(
        "https://api.mailgun.net/v3/domains/sandbox2f00e5e832a748ff80d76b2a13aaa5d8.mailgun.org/webhooks/click",
        auth=("api", "key-9f939581473944b38338d87cdb47c147"))
    print(g.status_code)
    prettify_json(g.json())

if __name__ == '__main__':
    get_webhooks()
    # get_unsubscribes()
    # get_bounce()
    # get_stats()
    # get_logs()
    # print(utils.parse_date(2018, 4, 17, 11, 21, 40, '+000'))
