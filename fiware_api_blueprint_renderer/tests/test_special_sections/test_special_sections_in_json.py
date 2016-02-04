# -*- coding: utf-8 -*-
import unittest
from os import path
import os
import sys
import shutil
import json
from subprocess import Popen, PIPE, call
import pprint
import codecs

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)


from tests.test_utils import *

special_section_test = None

data_test_path=os.path.dirname(path.abspath(__file__))+"/special_sections.json"

with open(data_test_path, 'r') as f:       
    special_section_test = json.load(f)


class TestSpecialSectionsInJSON(unittest.TestCase):
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

        with codecs.open('/var/tmp/fiware_api_blueprint_renderer_tmp/api_test.json', 'r', encoding='UTF-8') as f:
            doc = f.read()
            doc.decode(encoding="UTF-8")
            cls.out_json = json.loads(doc, encoding='UTF-8')


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



    def test_special_sections_in_json(self):
        
        _json_special_section = self.out_json["api_metadata"]["subsections"][0]["subsections"]
        _special_section = json.dumps(special_section_test)
        _special_section = json.loads(_special_section)
        self.assertEqual(len(_json_special_section), len(_special_section))
        for section in _json_special_section:
            expected_value = _special_section[section["id"]].encode('latin-1')
            obtained_value =section["body"].encode('latin-1')
            self.assertEqual(expected_value, obtained_value) 









suite = unittest.TestLoader().loadTestsFromTestCase(TestSpecialSectionsInJSON)
unittest.TextTestRunner(verbosity=2).run(suite)