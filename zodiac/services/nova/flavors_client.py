import json
import zodiac.common.rest_client as rest_client
import time

class FlavorsClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
        
    def list_flavors(self):
        return self.client.get('flavors')
        
    def list_flavors_with_details(self):
        return self.client.get('flavors/detail')
        
    def get_flavor_details(self, flavor_id):
        return self.client.delete("flavors/%s" % str(flavor_id))