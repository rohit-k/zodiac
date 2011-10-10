from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ImagesTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_create_image(self):
        pass
        
    def test_get_image(self):
        pass
        
    def test_delete_image(self):
        pass
        
    def test_list_images(self):
        pass
        
    def test_list_images_with_detail(self):
        pass
        
    def test_list_images_filter_by_type(self):
        pass
    
    def test_list_images_filter_by_name(self):
        pass
        
    def test_list_images_filter_by_server_ref(self):
        pass
        
    def test_list_images_filter_by_status(self):
        pass
        
    def test_list_images_filter_by_status(self):
        pass