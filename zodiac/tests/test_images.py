from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ImagesTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()        
        cls.servers_client = cls.os.servers_client
        cls.images_client = cls.os.images_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
        name = data_gen('server')
        resp, body = cls.servers_client.create_server(name, cls.image_ref, cls.flavor_ref)
        cls.id = body['server']['id']
        cls.servers_client.wait_for_server_status(cls.id, 'ACTIVE')
        
        name = data_gen('server')
        resp, body = cls.images_client.create_image(cls.id, name)
        cls.image_id = body['image']['id']
        cls.images_client.wait_for_image_status(cls.image_id)
        
    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_create_delete_image(self):
        """ An image of the given server should be created """
        name = data_gen('image')
        resp, body = self.images_client.create_image(self.id, name)
        image_id = body['image']['id']
        self.images_client.wait_for_image_status(image_id)
        
        resp, body = self.images_client.get_image(image_id)
        self.assertEqual(name, body['image']['name'])
        
        self.images_client.delete
        
    def test_get_image_details(self):
        """ The full details of the image are returned """
        self.client.get_image_details(self.image_id)
        
    def test_list_images(self):
        """ A list of all valid images should be returned """
        self.client.list_images()
        
    def test_list_images_with_detail(self):
        """ A detailed list of all valid images should be returned """
        self.client.list_images_with_detail()
        
    def test_list_images_filter_by_type(self):
        """ A list of images filtered by their type should be returned """
        self.client.list_images({'type' : 'BASE'})
    
    def test_list_images_filter_by_name(self):
        """ A list of images filtered by the provided name should be returned """
        self.client.list_images({'name' : 'Ubuntu'})
        
    def test_list_images_filter_by_server_ref(self):
        """ A list of images filtered by the provided server ref should be returned """
        self.client.list_images({'serverRef' : '2'})
        
    def test_list_images_filter_by_status(self):
        """ A list of images filtered by the provided server status should be returned """
        self.client.list_images({'status' : 'active'})
        
    def test_list_images_detailed_filter_by_status(self):
        """ A detailed list of images filtered by the provided server status should be returned """
        self.client.list_images_with_detail({'status' : 'active'})
        
    def test_list_images_filter_by_type(self):
        """ A detailed list of images filtered by their type should be returned """
        self.client.list_images_with_detail({'type' : 'BASE'})

    def test_list_images_filter_by_name(self):
        """ A detailed list of images filtered by the provided name should be returned """
        self.client.list_images_with_detail({'name' : 'Fedora'})

    def test_list_images_filter_by_server_ref(self):
        """ A detailed list of images filtered by the provided server ref should be returned """
        self.client.list_images_with_detail({'serverRef' : '2'})