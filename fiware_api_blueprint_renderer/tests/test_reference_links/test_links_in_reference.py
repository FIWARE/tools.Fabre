#! /usr/bin/env python

import os
from os import path
import json
from pprint import pprint
import shutil
from subprocess import Popen, PIPE, call
import unittest


class TestLinksReference(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pathname_ = path.dirname(path.abspath(__file__))
        cls.apib_file = pathname_+"/base.apib"
        cls.tmp_result_files = "/var/tmp/test-links-in-reference-160faf1aae1dd41c8f16746ea744f138"

        if os.path.exists(cls.tmp_result_files):
            shutil.rmtree(cls.tmp_result_files)

        os.makedirs(cls.tmp_result_files)

        Popen(["fabre", "-i", cls.apib_file, "-o", 
             cls.tmp_result_files, "--no-clear-temp-dir"], stdout=PIPE, stderr=PIPE).communicate()


        with open('/var/tmp/fiware_api_blueprint_renderer_tmp/base.json', 'r') as f:
            cls.out_json = json.load(f)


    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tmp_result_files):
            shutil.rmtree(cls.tmp_result_files)

        to_delete = ['/var/tmp/fiware_api_blueprint_renderer_tmp/base.apib',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/base.extras',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/base.json']

        for filename in to_delete:
            if os.path.exists(filename):
                os.remove(filename)


    def test_normal_link_in_abstract(self):
        
        json_link = {"url": "http://normal-link-in-abstract.com",\
                     "title": "normal-link-in-abstract"}

        self.assertIn(json_link, self.out_json["reference_links"])


    def test_direct_secure_link_in_abstract(self):
        
        json_link = {"url": "https://direct-secure-link-in-abstract.com",\
                     "title": "https://direct-secure-link-in-abstract.com"}

        self.assertIn(json_link, self.out_json["reference_links"])


    def test_direct_link_in_abstract(self):
        
        json_link ={"url": "http://direct-link-in-abstract.com",\
                    "title": "http://direct-link-in-abstract.com"}

        self.assertIn(json_link, self.out_json["reference_links"])

"""
    def test_link_with_quotes_in_abstract(self):
        
        
        json_link = {"url": "http://link-with-quotes.com?id=\"weird-id\"", \
                     "title": "http://link-with-quotes.com?id=\"weird-id\""}

        self.assertIn(json_link, self.out_json["reference_links"])
"""

suite = unittest.TestLoader().loadTestsFromTestCase(TestLinksReference)
unittest.TextTestRunner(verbosity=1).run(suite)