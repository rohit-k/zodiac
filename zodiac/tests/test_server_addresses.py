from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ServerAddressesTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
        name = data_gen('server')
        resp, body = cls.client.create_server(name, cls.image_ref, cls.flavor_ref)
        cls.id = body['server']['id']
        cls.client.wait_for_server_status(cls.id, 'ACTIVE')

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_server(cls.id)
        
    @attr(type='positive')
    def test_list_addresses(self):
        """ All public and private addresses for a server should be returned """
        
        resp, addresses = self.client.list_addresses(self.id)
        self.assertTrue(addresses['addresses']['public'][0]['addr'] != '')
        self.assertTrue(addresses['addresses']['public'][1]['addr'] != '')
        self.assertTrue(addresses['addresses']['private'][0]['addr'] != '')
        
    def test_list_addresses_by_network(self):
        """ Providing a network type should filter the addresses return by that type """
        
        resp, addresses = self.client.list_addresses_by_network(self.id, 'public')
        self.assertTrue(addresses['public'][0]['addr'] != '')
        self.assertTrue(addresses['public'][1]['addr'] != '')
        
        resp, addresses = self.client.list_addresses_by_network(self.id, 'private')
        self.assertTrue(addresses['private'][0]['addr'] != '')
        
