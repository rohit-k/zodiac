import json
import zodiac.common.rest_client as rest_client
import time

class ImagesClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
        
    def list_images(self):
        return self.client.get('images')
        
    def list_images_with_details(self):
        return self.client.get('images/detail')
        
    def get_image_details(self, image_id):
        return self.client.get("images/%s" % str(image_id))
        
    def delete_image(self, image_id):
        return self.client.delete("images/%s" % str(image_id))