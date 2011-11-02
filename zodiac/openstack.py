from zodiac.services.nova.json import servers_json_client
from zodiac.services.nova.json import images_json_client
from zodiac.services.nova.json import flavors_client
import zodiac.config

class Manager(object):

    def __init__(self):
        """
        Top level manager for all Openstack APIs
        """
        
        self.config = zodiac.config.ZodiacConfig()
        self.servers_client = servers_json_client.ServersClient(self.config.nova.username, self.config.nova.api_key, 
                                                                self.config.nova.auth_url, self.config.nova.tenant_name)
        self.flavors_client = flavors_client.FlavorsClient(self.config.nova.username, self.config.nova.api_key, 
                                                           self.config.nova.auth_url, self.config.nova.tenant_name)
        self.images_client = images_json_client.ImagesClient(self.config.nova.username, self.config.nova.api_key, 
                                                           self.config.nova.auth_url, self.config.nova.tenant_name)
                                                                
