from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class ServerActionsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        resp, server = cls.client.create_server('clienttest', 6, 1)
        cls.id = server['server']['id']
        cls.client.wait_for_server_status(cls.id, 'ACTIVE')

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_server(cls.id)
        
    def test_change_server_password(self):
        resp, body = self.client.change_password(self.id, 'newpass')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        #TODO: SSH in to verify the new password works
        
    def test_reboot_server_hard(self):
        #TODO: Add validation the server has been rebooted
        
        resp, body = self.client.change_password(self.id, 'HARD')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
    def test_reboot_server_soft(self):
        #TODO: Add validation the server has been rebooted
        
        resp, body = self.client.change_password(self.id, 'SOFT')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
    def test_rebuild_server(self):
        
        self.client.rebuild(self.id, 'rebuiltserver', 3)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('3', server['server']['image']['id'])
        
    def test_resize_server_confirm(self):
        self.client.resize(self.id, 2)
        self.client.wait_for_server_status(self.id, 'VERIFY_RESIZE')
        
        self.client.confirm_resize(self.id)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('3', server['server']['flavor']['id'])
        
    def test_resize_server_revert(self):
        resp, server = self.client.create_server('clienttest', 2, 3)
        id = server['server']['id']
        self.client.wait_for_server_status(id, 'ACTIVE')
        
        self.client.resize(id, 1)
        self.client.wait_for_server_status(id, 'VERIFY_RESIZE')
        
        self.client.revert_resize(id)
        self.client.wait_for_server_status(id, 'ACTIVE')
        
        resp, server = self.client.get_server(id)
        self.assertEqual('3', server['server']['flavor']['id'])
        
        self.client.delete_server(id)
    
