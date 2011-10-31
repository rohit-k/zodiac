from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ServerMetadataTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
        cls.meta = { 'test1' : 'value1', 'test2' : 'value2' }
        name = data_gen('server')
        resp, server = cls.client.create_server(name, cls.image_ref, cls.flavor_ref, meta=cls.meta)
        
        #Wait for the server to become active
        self.client.wait_for_server_status(server['id'], 'ACTIVE')

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_exceed_server_metadata_limit_on_create(self):
        """ 
        The amount of metadata items provided on server creation
        exceeds the compute provider's limit, the request should fail 
        """
        
        meta = { 'key1' : 'value1', 'key2' : 'value2', 'key3' : 'value3',
                'key4' : 'value4', 'key5' : 'value5', 'key6' : 'value6'}
        name = data_gen('server')
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref, meta=meta)
        
        self.assertEqual('413', resp['status'])
        
    def test_list_server_metadata(self):
        """ All metadata key/value pairs for a server should be returned """
        pass

    def test_set_server_metadata(self):
        pass

    def test_update_server_metadata(self):
        pass

    def test_get_server_metadata_item(self):
        """ The value for a specic metadata key should be returned """
        pass

    def test_set_server_metadata_item(self):
        """ The value provided for the given should be set for the server"""
        pass

    def test_delete_server_metadata_item(self):
        """ The metadata value/key pair should be deleted from the server """
        pass
        