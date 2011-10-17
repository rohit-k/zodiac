import json
import zodiac.common.rest_client as rest_client
import time

class ImagesClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
        
    def list_images(self, params=None):
        url = 'images'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))
                
            url = "images?" + "".join(param_list)
        
        resp, body = self.client.get(url)
        body = json.loads(body)
        return resp, body
        
    def list_images_with_detail(self, params=None):
        url = 'images/detail'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))
                
            url = "images/detail?" + "".join(param_list)
        
        resp, body = self.client.get(url)
        body = json.loads(body)
        return resp, body
        
    def get_image_details(self, image_id):
        resp, body = self.client.get("images/%s" % str(image_id))
        body = json.loads(body)
        return resp, body
        
    def delete_image(self, image_id):
        return self.client.delete("images/%s" % str(image_id))