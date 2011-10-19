from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config

class ImagesMetadataTest(unittest.TestCase):
    
    _multiprocess_shared_ = True
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_list_image_metadata(self):
        """ The list of metadata keys and values for the image are returned """
        pass
        
    def test_set_image_metadata(self):
        pass
        
    def test_update_image_metadata(self):
        pass
        
    def test_get_image_metadata_item(self):
        pass
        
    def test_set_image_metadata_item(self):
        pass
        
    def test_delete_image_metadata_item(self):
        pass