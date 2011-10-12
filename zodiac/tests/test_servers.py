from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ServersTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
    
    @attr(type='positive')
    def test_create_delete_server(self):
        meta = { 'hello' : 'world' }
        accessIPv4 = '1.1.1.1'
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta, accessIPv4=accessIPv4)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('1.1.1.1', server['server']['accessIPv4'])
        
        self.client.delete_server(self.id)
        
    def test_create_server_min_ram_not_met(self):
        """ 
        If the flavor for a server does not meet the server's minimum RAM requirements,
        the request should fail
        """
        
        pass
        
    def test_create_server_with_admin_password(self):
        """ 
        If an admin password is provided on server creation, the server's root
        password should be set to that password.
        """
        resp, server = self.client.create_server('clienttest', 6, 1, adminPass='testpassword')
        id = server['server']['id']
        self.assertEqual('testpassword', server['server']['adminPass'])
        
        self.client.wait_for_server_status(id, 'ACTIVE')
        self.client.delete_server(id)
        
    def test_create_server_with_personality(self):
        """ The server should be created and the provided file injected """
        #TODO: Check file permissions/group/etc
        pass
        
    def test_list_servers(self):
        """ All servers for the tenant should be returned """
        self.client.list_servers()
        
    def test_list_servers_filter_by_image(self):
        """ Filter the list of servers by image """
        params = {'imageRef', 6}
        self.client.list_servers(params)
     
    def test_list_servers_filter_by_flavor(self):
        """ Filter the list of servers by flavor """
        params = {'imageRef', 1}
        self.client.list_servers(params)  
    
    def test_list_servers_filter_by_server_name(self):
        """ Filter the list of servers by name """
        params = {'name', 'clienttest'}
        self.client.list_servers(params)
        
    def test_list_servers_filter_by_server_status(self):
        """ Filter the list of servers by server status """
        params = {'status', 'active'}
        self.client.list_servers(params)    
        
    def test_list_servers_with_detail(self):
        """ Return a detailed list of all servers """
        self.client.list_servers_with_detail()
        
    def test_list_servers_detailed_filter_by_image(self):
        """ Filter the detailed list of servers by image """
        params = {'imageRef', 6}
        self.client.list_servers_with_detail(params)

    def test_list_servers_detailed_filter_by_flavor(self):
        """ Filter the detailed list of servers by flavor """
        params = {'imageRef', 1}
        self.client.list_servers_with_detail(params)    

    def test_list_servers_detailed_filter_by_server_name(self):
        """ Filter the detailed list of servers by server name """
        params = {'name', 'clienttest'}
        self.client.list_servers_with_detail(params)

    def test_list_servers_detailed_filter_by_server_status(self):
        """ Filter the detailed list of servers by server status """
        params = {'status', 'active'}
        self.client.list_servers_with_detail(params)
        
    def test_get_server_details(self):
        """ Return the full details of a single server """
        self.client.get_server(self.id)
        
    def test_delete_server(self):
        """ Delete a single server from a tenant """
        #TODO: Also verify that images created from the deleted server are also deleted
        pass
    
    @attr(type='positive')
    def test_update_server_name(self):
        """ The server name should be changed to the the provided value """
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.update_server(self.id, name='newname')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('newname', server['server']['name'])
        self.client.delete_server(self.id)
        
    def test_update_server_metadata(self):
        """ The provided metadata should be added to the server's metadata """
        meta = { 'hello' : 'world' }
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        meta = { 'test' : 'data' }
        self.client.update_server(self.id, meta=meta)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('data', server['server']['metadata']['test'])
        self.client.delete_server(self.id)
    
    def test_update_access_server_address(self):
        """ The server's access addresses should reflect the provided values """
        
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        self.client.update_server(self.id, ipv4='1.1.1.1', ipv6='::babe:2.2.2.2')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('1.1.1.1', server['server']['accessIPv4'])
        self.assertEqual('::babe:2.2.2.2', server['server']['accessIPv6'])
        
        self.client.delete_server(self.id)
        

