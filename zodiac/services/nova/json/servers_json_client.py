import json
import zodiac.common.rest_client as rest_client
import time

class ServersClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
        
    def create_server(self, name, image_ref, flavor_ref, meta = None, personality = None):
        
        post_body = {
            'name': name,
            'imageRef': image_ref,
            'flavorRef': flavor_ref,
        }
        
        if meta != None:
            post_body['metadata'] = meta
        
        post_body = json.dumps({'server': post_body})
        resp, body = self.client.post('servers', post_body)
        print body
        body = json.loads(body)
        return resp, body
        
    def update_server(self, server_id, name):
        post_body = {
            'name' : name,
        }
        
        post_body = json.dumps({'server': post_body})
        resp, body = self.client.put("servers/%s" % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def get_server(self, server_id):
        resp, body = self.client.get("servers/%s" % str(server_id))
        body = json.loads(body)
        return resp, body
        
    def delete_server(self, server_id):
        return self.client.delete("servers/%s" % str(server_id))
        
    def list_servers(self):
        resp, body = self.client.get('servers')
        body = json.loads(body)
        return resp, body
        
    def list_servers_with_details(self):
        resp, body = self.client.get('servers/detail')
        body = json.loads(body)
        return resp, body
        
    def wait_for_server_status(self, server_id, status):
        resp, body = self.get_server(server_id)
        server_status = body['server']['status']
        
        while(server_status != status):
            time.sleep(5)
            resp, body = self.get_server(server_id)
            server_status = body['server']['status']
            
            if(server_status == 'ERROR'):
                raise
                
    def list_addresses(self, server_id):
        return self.client.get("servers/%s/ips" % str(server_id))
        
    def list_addresses_by_network(self, server_id, network_id):
        return self.client.get("servers/%s/ips/%s" % (str(server_id), network_id))
    
    def change_password(self, server_id, password):
        post_body = {
            'changePassword' : {
                'adminPass': password,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def reboot(self, server_id, reboot_type):
        post_body = {
            'reboot' : {
                'type': reboot_type,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def rebuild(self, server_id, name, image_ref):
        post_body = {
            'rebuild' : {
                'name': name,
                'imageRef' : image_ref
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def resize(self, server_id, flavor_ref):
        post_body = {
            'resize' : {
                'flavorRef': flavor_ref,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
    
    def confirm_resize(self, server_id):
        post_body = {
            'confirmResize' : null
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
    
    def revert_resize(self, server_id):
        post_body = {
            'revertResize' : null
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def create_image(self, server_id, image_name):
        post_body = {
            'createImage' : {
                'name': image_name,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
            
            
        