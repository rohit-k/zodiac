from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config

class FlavorsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.flavors_client
        
    def test_list_flavors(self):
        self.client.list_flavors()
        
    def test_list_flavors_with_detail(self):
        self.client.list_flavors_with_detail()
        
    def test_list_flavors_limit_by_min_ram(self):
        self.client.list_flavors({'minRam' : '512'})
        
    def test_list_flavors_limit_by_min_disk(self):
        """ The list of flavors should be filtered by their minimum disk requirement """
        self.client.list_flavors({'minDisk' : '30'})
        
    def test_list_flavors_detailed_limit_by_min_ram(self):
        self.client.list_flavors_with_detail({'minRam' : '512'})

    def test_list_flavors_detailed_limit_by_min_disk(self):
        """ The list of flavors should be filtered by their minimum disk requirement """
        self.client.list_flavors_with_detail({'minDisk' : '30'})
        
    def test_get_flavor(self):
        self.client.get_flavor_details(1)
        