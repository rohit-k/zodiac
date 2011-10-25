from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ServerActionsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
        resp, server = cls.client.create_server('clienttest', 6, 1)
        cls.id = server['server']['id']
        cls.client.wait_for_server_status(cls.id, 'ACTIVE')

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_server(cls.id)
        
    def test_change_server_password(self):
        """ The server's root password should be changed to the provided password """
        resp, body = self.client.change_password(self.id, 'newpass')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        #TODO: SSH in to verify the new password works
        
    def test_server_password_complexity_not_met(self):
        """ 
        If the provided password does not meet the image's server requirements,
        The request should fail
        """
        
        pass
        
    def test_reboot_server_hard(self):
        """ The server should be power cycled """
        #TODO: Add validation the server has been rebooted
        
        resp, body = self.client.change_password(self.id, 'HARD')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
    def test_reboot_server_soft(self):
        """ The server should be signaled to reboot gracefully """
        #TODO: Add validation the server has been rebooted
        
        resp, body = self.client.change_password(self.id, 'SOFT')
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
    def test_rebuild_server(self):
        """ The server should be rebuilt using the provided image """
        
        self.client.rebuild(self.id, 'rebuiltserver', 3)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        resp, server = self.client.get_server(self.id)
        self.assertEqual('3', server['server']['image']['id'])
        
        #All IPs should be the same, server ref should be the same
    
    def test_rebuild_with_new_name(self):
        """ The system should be rebuilt with the given image and name """
        pass
        
    def test_rebuild_with_metadata(self):
        """ 
        When the server is rebuilt with additional metadata, it should
        be appended to the existing metadata """
        pass
        
    def test_resize_server_confirm(self):
        """ 
        The server's RAM and disk space should be modified to that of
        the provided flavor 
        """
        
        self.client.resize(self.id, 2)
        self.client.wait_for_server_status(self.id, 'VERIFY_RESIZE')
        
        self.client.confirm_resize(self.id)
        self.client.wait_for_server_status(self.id, 'ACTIVE')
        
        resp, server = self.client.get_server(self.id)
        self.assertEqual('3', server['server']['flavor']['id'])
        
    def test_resize_server_revert(self):
        """ 
        The server's RAM and disk space should return to its original
        values after a resize is reverted 
        """
        
        resp, server = self.client.create_server('clienttest', 6, 1)
        id = server['server']['id']
        self.client.wait_for_server_status(id, 'ACTIVE')
        
        self.client.resize(id, 2)
        self.client.wait_for_server_status(id, 'VERIFY_RESIZE')
        
        self.client.revert_resize(id)
        self.client.wait_for_server_status(id, 'ACTIVE')
        
        resp, server = self.client.get_server(id)
        self.assertEqual('1', server['server']['flavor']['id'])
        
        self.client.delete_server(id)
    
