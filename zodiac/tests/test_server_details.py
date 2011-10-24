from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config

class ServerDetailsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
    def test_list_servers(self):
        """ All servers for the tenant should be returned """
        self.client.list_servers()

    def test_list_servers_filter_by_image(self):
        """ Filter the list of servers by image """
        params = {'imageRef' : 2}
        self.client.list_servers(params)

    def test_list_servers_filter_by_flavor(self):
        """ Filter the list of servers by flavor """
        params = {'flavorId' : 1}
        self.client.list_servers(params)  

    def test_list_servers_filter_by_server_name(self):
        """ Filter the list of servers by name """
        params = {'name' : 'clienttest'}
        self.client.list_servers(params)

    def test_list_servers_filter_by_server_status(self):
        """ Filter the list of servers by server status """
        params = {'status' : 'active'}
        self.client.list_servers(params)    

    def test_list_servers_with_detail(self):
        """ Return a detailed list of all servers """
        self.client.list_servers_with_detail()

    def test_list_servers_detailed_filter_by_image(self):
        """ Filter the detailed list of servers by image """
        params = {'imageRef' : 1}
        self.client.list_servers_with_detail(params)

    def test_list_servers_detailed_filter_by_flavor(self):
        """ Filter the detailed list of servers by flavor """
        params = {'flavorRef' : 1}
        self.client.list_servers_with_detail(params)    

    def test_list_servers_detailed_filter_by_server_name(self):
        """ Filter the detailed list of servers by server name """
        params = {'name' : 'clienttest'}
        self.client.list_servers_with_detail(params)

    def test_list_servers_detailed_filter_by_server_status(self):
        """ Filter the detailed list of servers by server status """
        params = {'status' : 'active'}
        self.client.list_servers_with_detail(params)

    def test_get_server_details(self):
        """ Return the full details of a single server """
        #self.client.get_server(self.id)