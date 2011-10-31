from lxml import objectify
from lxml import etree
import zodiac.common.rest_client as rest_client
import time
from zodiac import exceptions
import zodiac.config
import json

class ServersClient(object):

    def __init__(self, username, key, auth_url, tenant_name):
        self.client = rest_client.RestClient(username, key, auth_url, tenant_name)
        self.config = zodiac.config.ZodiacConfig()
        self.build_interval = self.config.nova.build_interval
        self.build_timeout = self.config.nova.build_timeout
        self.maker = objectify.ElementMaker(annotate=False)
        self.headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
        
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
        server = self.maker.server()
        server.set('name', name)
        server.set('imageRef', str(image_ref))
        server.set('flavorRef', str(flavor_ref))
        server.set('xmlns', 'http://docs.openstack.org/compute/api/v1.1')
        
        if adminPass != None:
            server.set('adminPass', adminPass)
            
        if accessIPv4 != None:
            server.set('accessIPv4', accessIPv4)
            
        if accessIPv6 != None:
            server.set('accessIPv6', accessIPv6)
        
        if meta != None:
            metadata = self.maker.metadata()    
            for key, value in meta.items():
                item = self.maker.meta(value, key=key)
                metadata.append(item)
            server.append(metadata)
            
        if personality != None:
            file_list = self.maker.personality() 
            for item in personality:
                file_item = self.maker.file(item['contents'], path=item['path'])
                file_list.append(file_item)
            server.append(file_list)
            
        
        post_body = '<?xml version="1.0" encoding="UTF-8"?>' + etree.tostring(server)
        resp, body = self.client.post('servers', post_body, self.headers)
        
        server = objectify.fromstring(body)
        body = dict(server.items())
        body['flavor'] = dict(server.flavor.items())
        body['image'] = dict(server.image.items())
        body['addresses'] = dict(server.addresses.items())
        
        return resp, body
        

    def update_server(self, server_id, name = None, meta = None, accessIPv4 = None, 
                      accessIPv6 = None):
        """
        Updates the properties of an existing server.
        server_id: The id of an existing server.
        name (optional): The name of the server.
        meta (optional): A dictionary of values to be used as metadata. 
        personality: A list of files to be injected into the server.
        ipv4: The IPv4 address of the server.
        ipv6: The IPv6 address of the server.
        """
        
        server = self.maker.server()
        server.set('xmlns', 'http://docs.openstack.org/compute/api/v1.1')
        
        if meta != None:
            metadata = self.maker.metadata()    
            for key, value in meta.items():
                item = self.maker.meta(value, key=key)
                metadata.append(item)
            server.append(metadata)
            
        if name != None:
            server.set('name', name)
        
        if accessIPv4 != None:
            server.set('accessIPv4', accessIPv4)
            
        if accessIPv6 != None:
            server.set('accessIPv6', accessIPv6)
        
        post_body = '<?xml version="1.0" encoding="UTF-8"?>' + etree.tostring(server)
        headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
        resp, body = self.client.put("servers/%s" % str(server_id), post_body, self.headers)
        server = objectify.fromstring(body)
        body = dict(server.items())
        body['flavor'] = dict(server.flavor.items())
        body['image'] = dict(server.image.items())
        body['addresses'] = dict(server.addresses.items())
        return resp, body
        
    def get_server(self, server_id):
        """Returns the properties of an existing server."""
        resp, body = self.client.get("servers/%s.xml" % str(server_id))
        server = objectify.fromstring(body)
        body = dict(server.items())
        body['flavor'] = dict(server.flavor.items())
        body['image'] = dict(server.image.items())
        body['addresses'] = dict(server.addresses.items())
        return resp, body

    def delete_server(self, server_id):
        """Deletes the given server."""
        return self.client.delete("servers/%s" % str(server_id))
        
    def list_servers(self, params = None):
        """Lists all servers for a tenant."""

        url = 'servers.xml'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))

            url = "servers.xml?" + "".join(param_list)

        resp, body = self.client.get(url)
        servers = objectify.fromstring(body)
        server_list = []
        
        for server in servers.getchildren():
            s = dict(server.items())
            server_list.append(s)
        return resp, server_list

    def list_servers_with_detail(self, params = None):
        """Lists all servers in detail for a tenant."""

        url = 'servers/detail.xml'
        if params != None:
            param_list = []
            for param, value in params.iteritems():
                param_list.append("%s=%s&" % (param, value))

            url = "servers/detail.xml?" + "".join(param_list)

        resp, body = self.client.get(url)
        
        servers = objectify.fromstring(body)
        server_list = []
        
        for server in servers.getchildren():
            s = dict(server.items())
            s['flavor'] = dict(server.flavor.items())
            s['image'] = dict(server.image.items())
            s['addresses'] = dict(server.addresses.items())
            server_list.append(s)
        return resp, server_list

    def wait_for_server_status(self, server_id, status):
        """Waits for a server to reach a given status."""
        resp, body = self.get_server(server_id)
        server_status = body['status']
        start = int(time.time())

        while(server_status != status):
            time.sleep(self.build_interval)
            resp, body = self.get_server(server_id)
            server_status = body['status']

            if(server_status == 'ERROR'):
                raise exceptions.BuildErrorException

            if (int(time.time()) - start >= self.build_timeout):
                raise exceptions.TimeoutException

    def list_addresses(self, server_id):
        """Lists all addresses for a server."""
        resp, body = self.client.get("servers/%s/ips.xml" % str(server_id))
        addresses = objectify.fromstring(body)
        
        #TODO (dwalleck): This is an awful hack. I'm tired, I'll fix this later
        address_resp = {'public' : None, 'private' : None}
        public_list = [{'addr' : addresses.getchildren()[0].getchildren()[1].get('addr'), 'version' : 4}, 
                      {'addr' : addresses.getchildren()[0].getchildren()[0].get('addr'), 'version' : 6}]
        private_list = [{'addr' : addresses.getchildren()[1].getchildren()[0].get('addr'), 'version' : 4}]
        address_resp['public'] = public_list
        address_resp['private'] = private_list
        
        return resp, address_resp

    def list_addresses_by_network(self, server_id, network_id):
        """Lists all addresses of a specific network type for a server."""
        resp, body = self.client.get("servers/%s/ips/%s.xml" % 
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
        return self.client.post('servers/%s/action' % str(server_id), self.headers, post_body)

    def reboot(self, server_id, reboot_type):
        """Reboots a server."""
        post_body = {
            'reboot' : {
                'type': reboot_type,
            }
        }

        post_body = json.dumps(post_body)
        return self.client.post('servers/%s/action' % str(server_id), self.headers, post_body)


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
                                      % str(server_id), self.headers, post_body)
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
                                      str(server_id), self.headers, post_body)
        return resp, body

    def confirm_resize(self, server_id):
        """Confirms the flavor change for a server."""
        post_body = {
            'confirmResize' : null
        }

        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), self.headers, post_body)
        return resp, body

    def revert_resize(self, server_id):
        """Reverts a server back to its original flavor."""
        post_body = {
            'revertResize' : null
        }

        post_body = json.dumps(post_body)
        resp, body = self.client.post('servers/%s/action' % 
                                      str(server_id), self.headers, post_body)
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
                                      str(server_id), self.headers, post_body)
        body = json.loads(body)
        return resp, body