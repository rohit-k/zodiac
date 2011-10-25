from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ImagesTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()        
        cls.client = cls.os.images_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_id = cls.config.env.image_ref
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    @unittest.skip('Not currently enabled')     
    def test_create_delete_image(self):
        name = data_gen('image')
        resp, body = self.images_client.create_image(self.id, name)
        image_id = body['image']['id']
        self.images_client.wait_for_image_status(image_id)
        
        resp, body = self.images_client.get_image(image_id)
        self.assertEqual(name, body['image']['name'])
        
        self.images_client.delete
        
    def test_get_image_details(self):
        resp, body = self.client.get_image_details(self.image_id)
        image = body['image']
        self.assertEqual(self.image_id, image['id'])
        
    def test_list_images(self):
        resp, body = self.client.list_images()
        images = body['images']
        
        found = False
        for image in images:
            if image['id'] == self.image_id:
                found = True
        
        self.assertTrue(found)
        
        
    def test_list_images_with_detail(self):
        resp, body = self.client.list_images_with_detail()
        images = body['images']
        
        found = False
        for image in images:
            if image['id'] == self.image_id:
                found = True
        self.assertTrue(found)
        
    def test_list_images_filter_by_type(self):
        resp, body = self.client.list_images({'type' : 'BASE'})
    
    def test_list_images_filter_by_name(self):
        self.client.list_images({'name' : 'Ubuntu'})
        
    def test_list_images_filter_by_server_ref(self):
        self.client.list_images({'serverRef' : self.image_id})
        
    def test_list_images_filter_by_status(self):
        self.client.list_images({'status' : 'active'})
        
    def test_list_images_detailed_filter_by_status(self):
        self.client.list_images_with_detail({'status' : 'active'})
        
    def test_list_images_detailed_filter_by_type(self):
        self.client.list_images_with_detail({'type' : 'BASE'})

    def test_list_images_detailed_filter_by_name(self):
        self.client.list_images_with_detail({'name' : 'Fedora'})

    def test_list_images_detailed_filter_by_server_ref(self):
        self.client.list_images_with_detail({'serverRef' : self.image_id})