
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


metadata_test = {
    "FORMAT": "1A",
    "HOST": "http://telefonicaid.github.io/fiware-orion/api/v2/",
    "TITLE": "FIWARE-NGSI v2 Specification",
    "DATE": "30 July 2015",
    "VERSION": "abcedefg",
    "PREVIOUS_VERSION": "jhdfgh",
    "APIARY_PROJECT": "test5950",
    "GITHUB_SOURCE": "http://github.com/telefonicaid/fiware-orion.git",
    "SPEC_URL": "http://example.com/api/"
}

class TestMetadataInJSON(unittest.TestCase):
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



    def test_metadata_in_json(self):
        
        self.assertEqual(len(self.out_json['metadata']), len(metadata_test))
        for metadatum in self.out_json['metadata']:             
            self.assertEqual(metadata_test[metadatum["name"]], metadatum["value"]) 









suite = unittest.TestLoader().loadTestsFromTestCase(TestMetadataInJSON)
unittest.TextTestRunner(verbosity=2).run(suite)