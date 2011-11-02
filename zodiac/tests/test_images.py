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
    
    @unittest.skip('Not currently enabled')     
    def test_create_delete_image(self):
        """ An image for the provided server should be created """
        name = data_gen('image')
        resp, body = self.client.create_image(self.id, name)
        image_id = body['image']['id']
        self.images_client.wait_for_image_status(image_id)
        
        #Verify the image was created correctly
        resp, body = self.images_client.get_image(image_id)
        self.assertEqual(name, body['image']['name'])
        
        #Teardown
        self.images_client.delete()
    
    @attr(type='smoke')    
    def test_get_image_details(self):
        resp, image = self.client.get_image(self.image_id)
        self.assertEqual(self.image_id, image['id'])
    
    @attr(type='smoke')    
    def test_list_images(self):
        """ The list of all images should contain the image flavor """
        resp, body = self.client.list_images()
        images = body['images']
        
        found = False
        for image in images:
            if image['id'] == self.image_id:
                found = True
        
        self.assertTrue(found)
        
    @attr(type='smoke')    
    def test_list_images_with_detail(self):
        """ Detailed list of all images should contain the expected image """
        resp, body = self.client.list_images_with_detail()
        images = body['images']
        
        found = False
        for image in images:
            if image['id'] == self.image_id:
                found = True
        self.assertTrue(found)