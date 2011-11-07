from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen
from zodiac.common import ssh
import base64
from zodiac import exceptions

class ServersTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        cls.ssh_timeout = cls.config.nova.ssh_timeout
    
    @attr(type='smoke')
    def test_server_name_blank(self):
        
        try:
            resp, server = self.client.create_server('', self.image_ref, 
                                                     self.flavor_ref)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Server name cannot be blank')
        
        #assert response = Server name is an empty string, 400
        
    @unittest.skip('not now')
    def test_server_name_special_chars(self):
        resp, server = self.client.create_server('com.test.server', 
                                                 self.image_ref, 
                                                 self.flavor_ref)
                                                 
        #Wait for the server to become active
        self.client.wait_for_server_status(server['id'], 'ACTIVE')
        
    def test_server_min_ram_not_met(self):
        
        try:
            resp, server = self.client.create_server('com.test.server', 13, 1)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Server minimum RAM was not met by flavor')
    
    @unittest.skip('not now')    
    def test_personality_file_name_blank(self):
        file_contents = 'This is a test file.'
        personality = [{'path' : '', 
                           'contents' : base64.b64encode(file_contents)}]
        resp, server = self.client.create_server('blankfile', 
                                                     self.image_ref, 
                                                     self.flavor_ref, 
                                                     personality=personality)
                                                     
    def test_personality_file_contents_not_encoded(self):
        file_contents = 'This is a test file.'
        personality = [{'path' : '/etc/testfile.txt', 
                            'contents' : file_contents}]
        
        try:
            resp, server = self.client.create_server('blankfile', 
                                                      self.image_ref, 
                                                      self.flavor_ref, 
                                                      personality=personality)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Unencoded file contents should not be accepted')
        
    @unittest.skip('not now')    
    def test_invalid_ip_v4_address(self):
        meta = { 'hello' : 'world' }
        accessIPv4 = '1.1.1.1.1.1'
        name = data_gen('server')
        file_contents = 'This is a test file.'
        personality = [{'path' : '/etc/test.txt', 
                       'contents' : base64.b64encode(file_contents)}]
        resp, server = self.client.create_server(name, 
                                                 self.image_ref, 
                                                 self.flavor_ref, 
                                                 accessIPv4=accessIPv4)
                                                 
    @unittest.skip('not now') 
    def test_invalid_ip_v6_address(self):
        accessIPv6 = '2.2.2.2'
        name = data_gen('server')
        resp, server = self.client.create_server(name, 
                                                  self.image_ref, 
                                                  self.flavor_ref, 
                                                  accessIPv6=accessIPv6)    