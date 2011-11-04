import httplib2
import json
import zodiac.config

class RestClient(object):
    
    def __init__(self, user, key, auth_url, tenant_name=None):
        self.config = zodiac.config.ZodiacConfig()
        
        if self.config.env.authentication == 'keystone':
            self.token, self.base_url = self.keystone_authenticate(user, 
                                                                   key, 
                                                                   auth_url, 
                                                                   tenant_name)
        else:
            self.token, self.base_url = self.keystone_authenticate(user, 
                                                                   key, 
                                                                   auth_url)
        
    def basic_authenticate(self, user, api_key):        
        """
        Provides authenitication for the target API
        """
        
        params = {}
        params['headers'] = {'User-Agent': 'Test-Client', 'X-Auth-User': user, 'X-Auth-Key': api_key}

        self.http_obj = httplib2.Http()
        resp, body = self.http_obj.request(self.auth_url, 'GET', **params)
        try:
            return resp['x-auth-token'], resp['x-server-management-url']
        except:
            raise
            
    def keystone_authenticate(self, user, api_key, auth_url, tenant_name):        
        """
        Provides authenitication via Keystone
        """
        
        creds = { 'auth' : {
                'passwordCredentials' : {
                    'username' : user,
                    'password' : api_key,
                },
                'tenantName': tenant_name
            }
        
        }
        
        self.http_obj = httplib2.Http()
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(creds)
        resp, body = self.http_obj.request(auth_url,'POST',headers=headers, body=body)
        
        try:
            auth_data = json.loads(body)['access']
            token = auth_data['token']['id']
            mgmt_url = auth_data['serviceCatalog'][0]['endpoints'][0]['publicURL']
            
            #TODO (dwalleck): This is a horrible stopgap. Need to join strings more cleanly
            temp = mgmt_url.rsplit('/')
            management_url = temp[0] + '//' + temp[2] + '/' + temp[3] + '/' + tenant_name
            return token, management_url
        except KeyError:
            print "Failed to authenticate user"
            raise
            
    def post(self, url, body, headers):
        return self.request('POST', url, headers, body)
        
    def get(self, url):
        return self.request('GET', url)
        
    def delete(self, url):
        return self.request('DELETE', url)
        
    def put(self, url, body, headers):
        return self.request('PUT', url, headers, body)
        
    def request(self, method, url, headers=None, body=None):
        """ A simple HTTP request interface."""
        
        self.http_obj = httplib2.Http()
        if headers == None:
            headers = {}
        headers['X-Auth-Token'] = self.token
        
        req_url = "%s/%s" % (self.base_url, url)    
        resp, body = self.http_obj.request(req_url, method, headers=headers, body=body)
        
        return resp, body
