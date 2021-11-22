'''
Created on 2021-11-21

@author: wf
'''
import unittest
from storage.weaviatestorage import Weaviate

class TestYaml(unittest.TestCase):
    '''
    test the docker compose yaml modification
    '''


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDockerComposeYaml(self):
        '''
        check that the port has been changed to 8090
        '''
        port=Weaviate.readPort()
        self.assertEqual(8090,port)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()