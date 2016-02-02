import unittest
from os import path
import os
import shutil
import sys
import json
from subprocess import Popen, PIPE, call
import pprint
from lxml import etree, objectify
from lxml.cssselect import CSSSelector
from pyquery import PyQuery as pq

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.order_uri import  order_uri_parameters, order_request_parameters
from tests.test_utils import *


class TestVersionLinks(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass
    
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    """
    
    """
    """
    @for_examples(
    ('api_test1', [
        'http://example.com/api/abcedefg',
        'http://example.com/api/jhdfgh',
        'http://example.com/api/latest'
        ]),
    ('api_test2', [
        'http://example.com/api/abcedefg',
        'http://example.com/api/latest'
        ]),
    ('api_test3', [
        'http://example.com/api/jhdfgh',
        'http://example.com/api/latest'
        ]),
    ('api_test4', []
    ),
    ('api_test5', []
    ),

    )
    """
    @for_examples(
    ('api_test1', [
        'http://example.com/api/abcedefg',
        'http://example.com/api/jhdfgh',
        'http://example.com/api/latest'
        ]),
    ('api_test2', [
        'http://example.com/api/abcedefg',
        'http://example.com/api/latest'
        ]),

    )

    def test_github_apiary_links(self, apib_file_name, expected_urls):

        self.render_apib(apib_file_name)
        
        sel = CSSSelector('div#top-source-buttons')

        versions_dd = self.pq("dd.versionValue")

        for version_dd in versions_dd:
            a_element = pq(version_dd).children("a")
            assert pq(a_element).attr["href"] in expected_urls
            expected_urls.remove(pq(a_element).attr["href"])

        self.assertEqual(len(expected_urls), 0)
        """
        links=self.pq('div#top-source-buttons').children()

        for link in links:
            try:
                url = expected_urls.pop(0)
            except IndexError as e:
                print "APIB has to much links in #top-source-buttons div"
                assert False
            except Exception as e:
                print e
                assert False
            self.assertEqual(pq(link).attr["href"], url)


        self.assertEqual(len(expected_urls), 0)
        """

        self.del_apib_files(apib_file_name)




    def del_apib_files(self,apib_file):
        if os.path.exists(self.tmp_result_files):
            shutil.rmtree(self.tmp_result_files)

        to_delete = ['/var/tmp/fiware_api_blueprint_renderer_tmp/'+apib_file+'.apib',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/'+apib_file+'.extras',
                     '/var/tmp/fiware_api_blueprint_renderer_tmp/'+apib_file+'.json']

        for filename in to_delete:
            if os.path.exists(filename):
                os.remove(filename)


    def render_apib(self,apib_file):
        pathname_ = path.dirname(path.abspath(__file__))
        self.apib_file = pathname_+"/"+apib_file+".apib"
        self.tmp_result_files = "/var/tmp/test-links-in-reference-160faf1aae1dd41c8f16746ea744f138"

        self.html_output = self.tmp_result_files+"/"+apib_file+".html"

        if os.path.exists(self.tmp_result_files):
            shutil.rmtree(self.tmp_result_files)

        os.makedirs(self.tmp_result_files)

        Popen(["fabre", "-i", self.apib_file, "-o", 
             self.tmp_result_files, "--no-clear-temp-dir"], stdout=PIPE, stderr=PIPE).communicate()

        parser = etree.HTMLParser()
        self.tree = etree.parse(""+self.tmp_result_files+"/"+apib_file+".html", parser)
        self.pq = pq(filename = self.tmp_result_files+"/"+apib_file+".html")

        with open('/var/tmp/fiware_api_blueprint_renderer_tmp/'+apib_file+'.json', 'r') as f:
            self.out_json = json.load(f)

suite = unittest.TestLoader().loadTestsFromTestCase(TestVersionLinks)
unittest.TextTestRunner(verbosity=2).run(suite)