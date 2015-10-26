
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


from tests.test_utils import *

test_data={
        "Action with attributes and without parent":
        {
            "get_with_body /v2":{"ambientNoise": 31.5},
            "get_without_body /v2": {"entities_url": "entityExample"}
        },
        "Action without attr but with resoruce attr":
        {
            "get_with_body /v2/entities":{"ambientNoise": 31.5},
            "get_without_body /v2/entities":{
                            "entities_url": "entityExample", 
                            "registrations_url": {
                                "second_level": {
                                    "thirdLevel": {
                                        "fourthLevel": "fourth level value"
                                    }
                                }
                            }
                        }

        },
        "action with attr link":
        {
            "get_with_body /v2/entities": {"ambientNoise": 31.5},
            "get_without_body /v2/entities":{
                                            "first_level": {
                                                "second_level": "stringValue",
                                                "third_level": {
                                                    "terString": "value3"
                                                }
                                            }, 
                                            "url": "aa"
                                            } 
        },
        "Action without attr but with resoruce link":
        {
            "get_with_body /v2/entities": {"ambientNoise": 31.5},
            "get_without_body /v2/entities": {
                                            "first_level": {
                                                "second_level": "stringValue", 
                                                "third_level": {
                                                    "terString": "value3"
                                                }
                                            }, 
                                            "url": "aa"
                                            }

        },
        "action with attr link":
        {
            "get_with_body /v2/entities":{"ambientNoise": 31.5},
            "get_without_body /v2/entities":{
                                            "first_level": {
                                                "second_level": "stringValue", 
                                                "third_level": {
                                                    "terString": "value3"
                                                }
                                            }, 
                                            "url": "aa"
                                            }
        },
        "attributes in request test":
        {
            "get_with_body /v2/entitiess":{"ambientNoise": 31.5},
            "get_without_body_but_attr /v2/entitiess":{"entities_url": "entityExampleREQ"},
            "get_without_body_but_attr_linked /v2/entitiess": {
                                                "first_level": {
                                                    "second_level": "stringValue", 
                                                    "third_level": {
                                                        "terString": "value3"
                                                    }
                                                }, 
                                                "url": "aa"
                                            }

        },
        "recursive attributes":
        {
            "get_recursive /v2/entitiesR":{
                                        "first_level": {
                                            "Country": "United Kingdom", 
                                            "city": "London", 
                                            "second_level": {
                                                "with_value": "defaultValue", 
                                                "third_level": {
                                                    "with_value": "value"
                                                }
                                            }
                                        }
                                    },
            "attribute_referencing_resource /v2/entitiesR":{
                                                "entities_url": "entityExample", 
                                                "registrations_url": {
                                                    "second_level": {
                                                        "thirdLevel": {
                                                            "fourthLevel": "fourth level value"
                                                        }
                                                    }
                                                }
                                            }
        }


    }




class TestPayloadInstantiationFromAPIB(unittest.TestCase):
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


    def test_payload_instantiation_json(self):
        
        for group in self.out_json['resourceGroups']:
            for resource in group['resources']:
                for action in resource['actions']: 
                   for example in action['examples']:
                        for request in example['requests']:
                            expected_value = test_data[action["name"]][request["name"]]

                            expected_value = json.dumps(expected_value, sort_keys=True, indent=4)

                            """ 
                            print "debug"
                            print expected_value
                            print request['body']
                            """
                            self.assertEqual(expected_value.strip(), request['body'].strip()) 









suite = unittest.TestLoader().loadTestsFromTestCase(TestPayloadInstantiationFromAPIB)
unittest.TextTestRunner(verbosity=2).run(suite)