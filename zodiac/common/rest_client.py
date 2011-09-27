import httplib2

class RestClient(object):
    
    def __init__(self, user, key, auth_url, base_url = None):
        self.user = user
        self.key = key
        self.auth_url = auth_url
        self.token, self.base_url = self.authenticate(user, key) 
        
    def authenticate(self, user, api_key):        
        """
        Provides authenitication for the target API
        """
        
        params = {}
        params['headers'] = {'User-Agent': 'Zodiac-Client', 'X-Auth-User': user, 'X-Auth-Key': api_key}

        self.http_obj = httplib2.Http()
        resp, body = self.http_obj.request(self.auth_url, 'GET', **params)
        try:
            return resp['x-auth-token'], resp['x-server-management-url']
        except:
            raise
            
    def post(self, url, body):
        return self.request('POST', url, body)
        
    def get(self, url):
        return self.request('GET', url)
        
    def delete(self, url):
        return self.request('DELETE', url)
        
    def put(self, url, body):
        return self.request('PUT', url, body)
        
    def request(self, method, url, body=None):
        """ A simple HTTP request interface."""
        
        self.http_obj = httplib2.Http()
        
        params = {}
        headers = {'Content-Type': 'application/json', 'X-Auth-Token': self.token}
        
        req_url = "%s/%s" % (self.base_url, url)    
        resp, body = self.http_obj.request(req_url, method, headers=headers, body=body)
        return resp, body
