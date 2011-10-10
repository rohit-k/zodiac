from zodiac.services.nova.json import servers_json_client

class Manager(object):

    def __init__(self):
        """
        Top level manager for all Openstack APIs
        TODO: Read user, key, auth_url from configuration file
        """
        
        self.servers_client = servers_json_client.ServersClient(user, key, 
                                                                url)
