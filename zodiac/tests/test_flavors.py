from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest

class FlavorsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_list_flavors(self):
        pass
        
    def test_list_flavors_with_detail(self):
        pass
        
    def test_list_flavors_limit_by_min_ram(self):
        pass
        
    def test_list_flavors_limit_by_min_disk(self):
        pass
        
    def test_get_flavor(self):
        pass
        