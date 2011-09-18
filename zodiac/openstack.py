from zodiac.services.nova.json import servers_json_client

class Manager(object):

    def __init__(self):
        self.servers_client = servers_json_client.ServersClient(user, key, auth_url)
