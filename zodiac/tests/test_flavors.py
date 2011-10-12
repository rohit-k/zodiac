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
        """ A list of valid flavors should be returned """
        pass
        
    def test_list_flavors_with_detail(self):
        """ A detailed list of valid flavors should be returned """
        pass
        
    def test_list_flavors_limit_by_min_ram(self):
        """ The list of flavors should be filtered by their minimum RAM requirement """
        pass
        
    def test_list_flavors_limit_by_min_disk(self):
        """ The list of flavors should be filtered by their minimum disk requirement """
        pass
        
    def test_get_flavor(self):
        """ The full details for the selected flavor should be returned """
        pass
        