from zodiac.services.nova.json import servers_json_client

class Manager(object):

    def __init__(self):
        """
        Top level manager for all Openstack APIs
        TODO: Read user, key, auth_url from configuration file
        """
        
        self.servers_client = servers_json_client.ServersClient('dwalleck', 'aacfe0a3-d0b6-4ecc-a469-912a6a629e6d', 'http://alpha.ord.servers.api.rackspacecloud.com:8774/v1.1')
