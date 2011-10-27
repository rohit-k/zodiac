from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen
from zodiac.common import ssh

class ServersTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
    
    @attr(type='smoke')
    def test_create_delete_server(self):
        meta = { 'hello' : 'world' }
        accessIPv4 = '1.1.1.1'
        accessIPv6 = '::babe:220.12.22.2'
        name = data_gen('server')
        resp, server = self.client.create_server(name, 
                                                 self.image_ref, 
                                                 self.flavor_ref, 
                                                 meta=meta, 
                                                 accessIPv4=accessIPv4,
                                                 accessIPv6=accessIPv6)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, body = self.client.get_server(self.id)
        server = body['server']
        self.assertEqual('1.1.1.1', server['accessIPv4'])
        self.assertEqual('::babe:220.12.22.2', server['accessIPv6'])
        self.assertEqual(name, server['name'])
        self.assertEqual(self.image_ref, server['image']['id'])
        self.assertEqual(str(self.flavor_ref), server['flavor']['id'])
        
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
        
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, 
                                               self.flavor_ref, adminPass='testpassword')
        
        server = body['server']
        self.assertEqual('testpassword', server['adminPass'])
        
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        self.client.delete_server(server['id'])
        
    def test_create_server_with_personality(self):
        """ The server should be created and the provided file injected """
        #TODO: Check file permissions/group/etc
        pass
        
    def test_delete_server(self):
        """ Delete a single server from a tenant """
        #TODO: Also verify that images created from the deleted server are also deleted
        pass
    
    @attr(type='smoke')
    def test_update_server_name(self):
        """ The server name should be changed to the the provided value """
        
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref)
        server = body['server']
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        self.client.update_server(server['id'], name='newname')
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        resp, body = self.client.get_server(server['id'])
        server = body['server']
        self.assertEqual('newname', server['name'])
        
        self.client.delete_server(self.id)
    
    @unittest.skip('May not be valid test case')     
    def test_update_server_metadata(self):
        """ The provided metadata should be added to the server's metadata """
        meta = { 'hello' : 'world' }
        name = data_gen('server')
        resp, body = self.client.create_server(name, 
                                               self.image_ref, 
                                               self.flavor_ref, 
                                               meta=meta)
        server = body['server']
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        meta = { 'test' : 'data' }
        self.client.update_server(server['id'], meta=meta)
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        resp, body = self.client.get_server(server['id'])
        server = body['server']
        self.assertEqual('data', server['metadata']['test'])
        
        self.client.delete_server(server['id'])
    
    def test_update_access_server_address(self):
        """ The server's access addresses should reflect the provided values """
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref)
        server = body['server']
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        self.client.update_server(server['id'], accessIPv4='1.1.1.1', accessIPv6='::babe:2.2.2.2')
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        resp, body = self.client.get_server(server['id'])
        server = body['server']
        self.assertEqual('1.1.1.1', server['accessIPv4'])
        self.assertEqual('::babe:2.2.2.2', server['accessIPv6'])
        
        self.client.delete_server(server['id'])
        

