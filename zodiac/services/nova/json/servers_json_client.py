import json
import zodiac.common.rest_client as rest_client
import time

class ServersClient(object):

    def __init__(self, username, key, auth_url):
        self.client = rest_client.RestClient(username, key, auth_url)
        
    def create_server(self, name, image_ref, flavor_ref, meta = None, 
                      personality = None, accessIPv4 = None, accessIPv6 = None,
                      adminPass = None):
        """
        Creates an instance of a server.
        name: The name of the server.
        image_ref: The reference to the image used to build the server.
        flavor_ref: The flavor used to build the server.
        meta: A dictionary of values to be used as metadata. 
        The limit is 5 key/values.
        personality: A list of dictionaries for files to be injected into 
        the server.
        """
        
        post_body = {
            'name': name,
            'imageRef': image_ref,
            'flavorRef': flavor_ref,
        }
        
        if meta != None:
            post_body['metadata'] = meta
            
        if personality != None:
            post_body['personality'] = personality
            
        if adminPass != None:
            post_body['adminPass'] = adminPass
            
        if accessIPv4 != None:
            post_body['accessIPv4'] = accessIPv4
            
        if accessIPv6 != None:
            post_body['accessIPv6'] = accessIPv6
        
        post_body = json.dumps({'server': post_body})
        resp, body = self.client.post('servers', post_body)
        body = json.loads(body)
        return resp, body
        
    def update_server(self, server_id, name = None, meta = None, ipv6 = None, 
                      ipv4 = None):
        """
        Updates the properties of an existing server.
        server_id: The id of an existing server.
        name (optional): The name of the server.
        meta (optional): A dictionary of values to be used as metadata. 
        personality: A list of files to be injected into the server.
        ipv4: The IPv4 address of the server.
        ipv6: The IPv6 address of the server.
        """
        
        post_body = {}
        
        if meta != None:
            post_body['metadata'] = meta
            
        if name != None:
            post_body['name'] = name
        
        if ipv6 != None:
            post_body['accessIPv6'] = ipv6
            
        if ipv4 != None:
            post_body['accessIPv4'] = ipv4
        
        post_body = json.dumps({'server': post_body})
        resp, body = self.client.put("servers/%s" % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def get_server(self, server_id):
        """Returns the properties of an existing server."""
        resp, body = self.client.get("servers/%s" % str(server_id))
        body = json.loads(body)
        return resp, body
        
    def delete_server(self, server_id):
        """Deletes the given server."""
        return self.client.delete("servers/%s" % str(server_id))
        
    def list_servers(self, params = None):
        """Lists all servers for a tenant."""
        
        url = 'servers'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))
                
            url = "servers?" + "".join(param_list)
        
        resp, body = self.client.get(url)
        body = json.loads(body)
        return resp, body
        
    def list_servers_with_detail(self, params = None):
        """Lists all servers in detail for a tenant."""
        
        url = 'servers/detail'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))
                
            url = "servers?" + "".join(param_list)
        
        resp, body = self.client.get(url)
        body = json.loads(body)
        return resp, body
        
        
        resp, body = self.client.get('servers/detail')
        body = json.loads(body)
        return resp, body
        
    def wait_for_server_status(self, server_id, status):
        """Waits for a server to reach a given status."""
        resp, body = self.get_server(server_id)
        server_status = body['server']['status']
        start = int(time.time())
        
        while(server_status != status):
            time.sleep(5)
            resp, body = self.get_server(server_id)
            server_status = body['server']['status']
            
            if(server_status == 'ERROR'):
                raise
                
            if (int(time.time()) - start >= 600):
                raise
                
    def list_addresses(self, server_id):
        """Lists all addresses for a server."""
        resp, body = self.client.get("servers/%s/ips" % str(server_id))
        body = json.loads(body)
        return resp, body
        
    def list_addresses_by_network(self, server_id, network_id):
        """Lists all addresses of a specific network type for a server."""
        resp, body = self.client.get("servers/%s/ips/%s" % 
                                    (str(server_id), network_id))
        body = json.loads(body)
        return resp, body
    
    def change_password(self, server_id, password):
        """Changes the root password for the server."""
        post_body = {
            'changePassword' : {
                'adminPass': password,
            }
        }
        
        post_body = json.dumps(post_body)
        return self.client.post('servers/%s/action' % str(server_id), post_body)
        
    def reboot(self, server_id, reboot_type):
        """Reboots a server."""
        post_body = {
            'reboot' : {
                'type': reboot_type,
            }
        }
        
        post_body = json.dumps(post_body)
        return self.client.post('servers/%s/action' % str(server_id), post_body)

        
    def rebuild(self, server_id, image_ref, name = None):
        """Rebuilds a server with a new image."""
        post_body = {
            'rebuild' : {
                'imageRef' : image_ref,
            }
        }
        
        if name != None:
            post_body['name'] = name
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' 
                                      % str(server_id), post_body)
        body = json.loads(body)
        return resp, body
        
    def resize(self, server_id, flavor_ref):
        """Changes the flavor of a server."""
        post_body = {
            'resize' : {
                'flavorRef': flavor_ref,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), post_body)
        return resp, body
    
    def confirm_resize(self, server_id):
        """Confirms the flavor change for a server."""
        post_body = {
            'confirmResize' : null
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), post_body)
        return resp, body
    
    def revert_resize(self, server_id):
        """Reverts a server back to its original flavor."""
        post_body = {
            'revertResize' : null
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), post_body)
        return resp, body
        
    def create_image(self, server_id, image_name):
        """Creates an image of the given server."""
        post_body = {
            'createImage' : {
                'name': image_name,
            }
        }
        
        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), post_body)
        body = json.loads(body)
        return resp, body
            
            
        
