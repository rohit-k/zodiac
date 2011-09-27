from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ServersTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_server(cls.id)
    
    @attr(type='positive')
    def test_create_delete_server(self):
        meta = { 'hello' : 'world' }
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.delete_server(self.id)
    
    @attr(type='positive')
    def test_update_server_name(self):
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.update_server(self.id, name='newname')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('newname', server['server']['name'])
        self.client.delete_server(self.id)
        
    def test_update_server_metadata(self):
        meta = { 'hello' : 'world' }
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        meta = { 'test' : 'data' }
        self.client.update_server(self.id, meta=meta)
        resp, server = self.client.get_server(self.id)
        self.assertEqual('data', server['server']['metadata']['test'])
        self.client.delete_server(self.id)
    
    def test_update_server_address(self):
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        self.client.update_server(self.id, ipv4='1.1.1.1', ipv6='::babe:2.2.2.2')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('1.1.1.1', server['server']['addresses']['public'][0]['addr'])
        self.assertEqual('::babe:2.2.2.2', server['server']['addresses']['public'][1]['addr'])
        
        self.client.delete_server(self.id)
        

