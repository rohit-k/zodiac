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
        """ An image of the given server should be created """
        pass
        
    def test_get_image(self):
        """ The full details of the image are returned """
        pass
        
    def test_delete_image(self):
        """ The given image should be deleted """
        pass
        
    def test_list_images(self):
        """ A list of all valid images should be returned """
        pass
        
    def test_list_images_with_detail(self):
        """ A detailed list of all valid images should be returned """
        pass
        
    def test_list_images_filter_by_type(self):
        """ A list of images filtered by their type should be returned """
        pass
    
    def test_list_images_filter_by_name(self):
        """ A list of images filtered by the provided name should be returned """
        pass
        
    def test_list_images_filter_by_server_ref(self):
        """ A list of images filtered by the provided server ref should be returned """
        pass
        
    def test_list_images_filter_by_status(self):
        """ A list of images filtered by the provided server status should be returned """
        pass
        
    def test_list_images_detailed_filter_by_status(self):
        """ A detailed list of images filtered by the provided server status should be returned """
        pass
        
    def test_list_images_filter_by_type(self):
        """ A detailed list of images filtered by their type should be returned """
        pass

    def test_list_images_filter_by_name(self):
        """ A detailed list of images filtered by the provided name should be returned """
        pass

    def test_list_images_filter_by_server_ref(self):
        """ A detailed list of images filtered by the provided server ref should be returned """
        pass