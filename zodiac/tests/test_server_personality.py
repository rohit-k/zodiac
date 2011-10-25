from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config

class ServerPersonalityTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client

    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_personality_file_already_exists(self):
        pass
        
    def test_personality_file_contents_exceeds_limit(self):
        pass
        
    def test_personality_file_path_exceeds_limit(self):
        pass

