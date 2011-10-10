from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ServerMetadataTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_exceed_server_metadata_limit_on_create(self):
        pass
        
    def test_list_server_metadata(self):
        pass

    def test_set_server_metadata(self):
        pass

    def test_update_server_metadata(self):
        pass

    def test_get_server_metadata_item(self):
        pass

    def test_set_server_metadata_item(self):
        pass

    def test_delete_server_metadata_item(self):
        pass
        