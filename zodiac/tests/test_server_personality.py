from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen
import base64

class ServerPersonalityTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        
    def test_personality_file_already_exists(self):
        pass
        
    def test_personality_files_exceed_limit(self):
        name = data_gen('server')
        file_contents = 'This is a test file.'
        personality = [{'path' : '/etc/test1.txt', 'contents' : base64.b64encode(file_contents)},
                        {'path' : '/etc/test2.txt', 'contents' : base64.b64encode(file_contents)},
                        {'path' : '/etc/test3.txt', 'contents' : base64.b64encode(file_contents)},
                        {'path' : '/etc/test4.txt', 'contents' : base64.b64encode(file_contents)},
                        {'path' : '/etc/test5.txt', 'contents' : base64.b64encode(file_contents)},
                        {'path' : '/etc/test6.txt', 'contents' : base64.b64encode(file_contents)}]
        
        resp, body = self.client.create_server(name, self.image_ref, self.flavor_ref, personality=personality)
        self.assertEqual('413', resp['status'])
        self.assertEqual('Personality file limit exceeded', body['overLimit']['message'])
        
    def test_personality_file_contents_exceeds_limit(self):
        pass
        
    def test_personality_file_path_exceeds_limit(self):
        pass

