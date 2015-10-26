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
import copy

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)


from tests.test_utils import *



class TestAdditionalSectionsInJSON(unittest.TestCase):
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


        data_test_path=os.path.dirname(path.abspath(__file__))+"/additional_sections.json"

        with open(data_test_path, 'r') as f:       
            cls.additional_section_test = json.load(f)

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



    def test_additional_sections_in_json(self):
        
        _json_sections = self.out_json["api_metadata"]["subsections"]

        _json_test = copy.deepcopy(self.additional_section_test)
        
        self.check_and_remove_section_from_json(_json_sections, _json_test)

        self.assertEqual(0,len( _json_test))


    def check_and_remove_section_from_json(self, subsections,expected_values):
        for subsection in subsections:
            self.assertEqual(expected_values[subsection["id"]],
                subsection["body"])
            if len(subsection["subsections"]):
                self.check_and_remove_section_from_json(subsection["subsections"], expected_values)
            del expected_values[subsection["id"]]



    def generate_test_example_base(self):
        _json={}
        subsections = self.out_json["api_metadata"]["subsections"]

        add_subsections_to_json(subsections,_json)

        data_test_path=os.path.dirname(path.abspath(__file__))+"/additional_sections.json"
        #pprint.pprint(_json)
        with open(data_test_path, "w") as outfile:
            json.dump(_json, outfile, indent=4)
      


def add_subsections_to_json(subsections,json_var):

    for subsection in subsections:
        #print subsection["id"]
        json_var[subsection["id"]]=subsection["body"]
        if len(subsection["subsections"]):
            add_subsections_to_json(subsection["subsections"], json_var)
    #print json_var



suite = unittest.TestLoader().loadTestsFromTestCase(TestAdditionalSectionsInJSON)
unittest.TextTestRunner(verbosity=2).run(suite)