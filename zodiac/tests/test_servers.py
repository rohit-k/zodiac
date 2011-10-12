from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ServersTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
    
    @attr(type='positive')
    def test_create_delete_server(self):
        meta = { 'hello' : 'world' }
        accessIPv4 = '1.1.1.1'
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta, accessIPv4=accessIPv4)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('1.1.1.1', server['server']['accessIPv4'])
        
        self.client.delete_server(self.id)
        
    def test_create_server_min_ram_not_met(self):
        pass
        
    def test_create_server_with_admin_password(self):
        resp, server = self.client.create_server('clienttest', 6, 1, adminPass='testpassword')
        id = server['server']['id']
        self.assertEqual('testpassword', server['server']['adminPass'])
        
        self.client.wait_for_server_status(id, 'ACTIVE')
        self.client.delete_server(id)
        
    def test_create_server_with_personality(self):
        #TODO: Check file permissions/group/etc
        pass
        
    def test_list_servers(self):
        self.client.list_servers()
        
    def test_list_servers_filter_by_image(self):
        pass
     
    def test_list_servers_filter_by_flavor(self):
        pass    
    
    def test_list_servers_filter_by_server_name(self):
        pass
        
    def test_list_servers_filter_by_server_status(self):
        pass    
        
    def test_list_servers_with_detail(self):
        self.client.list_servers_with_details()
        
    def test_list_servers_detailed_filter_by_image(self):
        pass

    def test_list_servers_detailed_filter_by_flavor(self):
        pass    

    def test_list_servers_detailed_filter_by_server_name(self):
        pass

    def test_list_servers_detailed_filter_by_server_status(self):
        pass
        
    def test_get_server_details(self):
        pass
        
    def test_delete_server(self):
        #TODO: Also verify that images created from the deleted server are also deleted
        pass
    
    @attr(type='positive')
    def test_update_server_name(self):
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        self.client.update_server(self.id, name='newname')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('newname', server['server']['name'])
        self.client.delete_server(self.id)
        
    def test_update_server_metadata(self):
        meta = { 'hello' : 'world' }
        resp, server = self.client.create_server('clienttest', 6, 1, meta=meta)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        meta = { 'test' : 'data' }
        self.client.update_server(self.id, meta=meta)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('data', server['server']['metadata']['test'])
        self.client.delete_server(self.id)
    
    def test_update_access_server_address(self):
        resp, server = self.client.create_server('clienttest', 6, 1)
        self.id = server['server']['id']
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        self.client.update_server(self.id, ipv4='1.1.1.1', ipv6='::babe:2.2.2.2')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('1.1.1.1', server['server']['accessIPv4'])
        self.assertEqual('::babe:2.2.2.2', server['server']['accessIPv6'])
        
        self.client.delete_server(self.id)
        

