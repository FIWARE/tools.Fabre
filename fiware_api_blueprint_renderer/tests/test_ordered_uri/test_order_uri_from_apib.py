
import unittest
from os import path
import os
import sys
import shutil
import json
from subprocess import Popen, PIPE, call
import pprint

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.order_uri import  order_uri_parameters, order_request_parameters
from tests.test_utils import *


class TestOrderURIFromAPIB(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass

    @classmethod
    def setUpClass(cls):
        pathname_ = path.dirname(path.abspath(__file__))
        cls.apib_file = pathname_+"/api_test.apib"
        cls.tmp_result_files = "/var/tmp/test-links-in-reference-160faf1aae1dd41c8f16746ea744f138"

        if os.path.exists(cls.tmp_result_files):
            shutil.rmtree(cls.tmp_result_files)

        os.makedirs(cls.tmp_result_files)

        Popen(["fabre", "-i", cls.apib_file, "-o", 
             cls.tmp_result_files, "--no-clear-temp-dir"], stdout=PIPE, stderr=PIPE).communicate()

        with open('/var/tmp/fiware_api_blueprint_renderer_tmp/api_test.json', 'r') as f:
            cls.out_json = json.load(f)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tmp_result_files):
            shutil.rmtree(cls.tmp_result_files)

        to_delete = ['/var/tmp/fiware_api_blueprint_renderer_tmp/api_test.apib',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/api_test.extras',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/api_test.json']

        for filename in to_delete:
            if os.path.exists(filename):
                os.remove(filename)


    def check_all_actions_equals_in_group(self,group,expected_value,occurrences):

        found = 0
        for resource in group['resources']:
            for action in resource['actions']:
                for example in action['examples']:
                    for request in example['requests']:
                        self.assertEqual(expected_value, request['name'].strip())
                        found = found +1

        self.assertEqual(occurrences,found)

    def check_exist_actions_in_group(self, group,expected_value, occurrences):
        found = 0
        for resource in group['resources']:
            for action in resource['actions']:
                for example in action['examples']:
                    for request in example['requests']:
                        if expected_value == request['name'].strip():
                            found = found +1

        self.assertEqual(occurrences,found)
    

    def test_order_request_parameters_from_json(self):
        

        for group in self.out_json['resourceGroups']:
            if "Root" == group['name']:
                self.check_all_actions_equals_in_group(group,"/v2",2)
            
            elif "Entities" == group['name']:
                self.check_all_actions_equals_in_group(group,"/v2/entities?id=foo&limit=10&options=bar",2)
            
            elif "AutoInstantiateEntities" == group['name']:
                self.check_exist_actions_in_group(group,"/v2/entities2{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}",1)
                self.check_exist_actions_in_group(group,"/v2/entities2",1)
            
            elif "instantiate with values" == group['name']:
                self.check_exist_actions_in_group(group,"/v2/entities2{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}",1)
                self.check_exist_actions_in_group(group,"/v2/entities2/?limit=100&offset=101",1)
            else:
                print "unexpected group", group['name']
                assert False
        

    
    def test_order_action_uri_parameters_for_json(self):

        expected_uris = ['/v2', 
        '/v2/entities{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}',
        '/v2/entities2{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}',
        '/v2/entities2/{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}'
        ]

        for group in self.out_json['resourceGroups']:
            for resource in group['resources']:
                for action in resource['actions']:
                    try:
                        expected_uris.remove(action['attributes']['uriTemplate'])
                    except Exception as e:
                        print "Error trying to remove ", action['attributes']['uriTemplate']
                        print e
                        assert False

        if len(expected_uris) > 0:
            print "Some URIs have not been found"
            print expected_uris
            assert False

        assert True


    def test_order_resource_uri_parameters_for_json(self):

        expected_uris = ['/v2/entities{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}', 
        '/v2/entities2{?attrs,coords,geometry,id,idPattern,limit,offset,options,q,type}',
        '/v2/entities3{?limit,offset}',
        '/v2'
        ]

        for group in self.out_json['resourceGroups']:
            for resource in group['resources']:
                try:
                    expected_uris.remove(resource['uriTemplate'])
                except Exception as e:
                    print "Error trying remove ", resource['uriTemplate']
                    print e
                    assert False

        if len(expected_uris) > 0:
            print "Some URIs have not been found"
            print expected_uris
            assert False

        assert True




suite = unittest.TestLoader().loadTestsFromTestCase(TestOrderURIFromAPIB)
unittest.TextTestRunner(verbosity=2).run(suite)