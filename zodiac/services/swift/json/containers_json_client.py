import json
import zodiac.common.rest_client as rest_client

class ContainersClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
