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
        
        #Wait for the server to become active
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        #Verify the specified attributes are set correctly
        resp, body = self.client.get_server(self.id)
        server = body['server']
        self.assertEqual('1.1.1.1', server['accessIPv4'])
        self.assertEqual('::babe:220.12.22.2', server['accessIPv6'])
        self.assertEqual(name, server['name'])
        self.assertEqual(self.image_ref, server['image']['id'])
        self.assertEqual(str(self.flavor_ref), server['flavor']['id'])
        
        #Teardown
        self.client.delete_server(self.id)
        
    def test_create_server_with_admin_password(self):
        """ 
        If an admin password is provided on server creation, the server's root
        password should be set to that password.
        """
        
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, 
                                               self.flavor_ref, adminPass='testpassword')
        
        #Verify the password is set correctly in the response
        server = body['server']
        self.assertEqual('testpassword', server['adminPass'])
        
        #SSH into the server using the set password
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        #Teardown
        self.client.delete_server(server['id'])
        
    def test_create_server_with_personality(self):
        """ The server should be created and the provided file injected """
        #TODO: Check file permissions/group/etc
        pass
    
    def test_update_server_name(self):
        """ The server name should be changed to the the provided value """
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref)
        server = body['server']
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        #Update the server with a new name
        self.client.update_server(server['id'], name='newname')
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        #Verify the name of the server has changed
        resp, body = self.client.get_server(server['id'])
        server = body['server']
        self.assertEqual('newname', server['name'])
        
        #Teardown
        self.client.delete_server(self.id)
    
    def test_update_access_server_address(self):
        """ The server's access addresses should reflect the provided values """
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref)
        server = body['server']
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        #Update the IPv4 and IPv6 access addresses
        self.client.update_server(server['id'], accessIPv4='1.1.1.1', accessIPv6='::babe:2.2.2.2')
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
        #Verify the access addresses have been updated
        resp, body = self.client.get_server(server['id'])
        server = body['server']
        self.assertEqual('1.1.1.1', server['accessIPv4'])
        self.assertEqual('::babe:2.2.2.2', server['accessIPv6'])
        
        #Teardown
        self.client.delete_server(server['id'])
        

