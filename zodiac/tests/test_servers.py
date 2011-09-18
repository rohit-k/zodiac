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
        pass
    
    @attr(type='positive')
    def test_create_delete_server(self):
        server = self.client.create_server('clienttest', 2, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.delete_server(self.id)
    
    @attr(type='positive')
    def test_update_server(self):
        server = self.client.create_server('clienttest', 2, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.update_server(name='newname')
        resp, server = self.client.get_server(self.id)
        print server['server']['name']
        self.client.delete_server(self.id)

