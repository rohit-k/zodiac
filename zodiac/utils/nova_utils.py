from zodiac import openstack
import zodiac.config

class NovaUtils : 
        
        def setUp(self):
            self.os = openstack.Manager()
            self.client = self.os.servers_client
            self.config = zodiac.config.ZodiacConfig()
            self.image_ref = self.config.env.image_ref
            self.flavor_ref = self.config.env.flavor_ref
            self.ssh_timeout = self.config.nova.ssh_timeout
            
        def delete_all_servers(self):
            """Utility to delete all servers for a particular tenant"""
            self.setUp()            
            resp,servers = self.client.list_servers()
            for server in servers['servers']:
                self.client.delete_server(server['id'])
            
   

       
        

 
    