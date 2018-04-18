import requests

class Event:
    def __init__(self,domain, auth_key):
        self.domain = domain
        self.auth_key = auth_key

    def get_log(self,)