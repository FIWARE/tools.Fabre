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
import pprint
from pyquery import PyQuery as pq

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.order_uri import  order_uri_parameters, order_request_parameters
from tests.test_utils import *
from src.renderer import main


class TestParametersHTML(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass
    
    @classmethod
    def setUpClass(cls):
        pathname_ = path.dirname(path.abspath(__file__))
        cls.apib_file = pathname_+"/api_test.apib"
        cls.tmp_result_files = "/var/tmp/test-links-in-reference-160faf1aae1dd41c8f16746ea744f138"

        cls.html_output = cls.tmp_result_files+"api_test.html"

        if os.path.exists(cls.tmp_result_files):
            shutil.rmtree(cls.tmp_result_files)

        os.makedirs(cls.tmp_result_files)

        main(["fabre", "-i", cls.apib_file, "-o", 
             cls.tmp_result_files, "--no-clear-temp-dir"])

        parser = etree.HTMLParser()
        cls.tree = etree.parse(""+cls.tmp_result_files+"/api_test.html", parser)
        cls.pq = pq(filename = cls.tmp_result_files+"/api_test.html")

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


    def test_parameters_name_order(self):


        parameters_dl = self.pq(".parameters-title+dl")
        

        check_parameter_dl_order(parameters_dl)
        
    
    def test_parameters_payload_name_order(self):


        payloads_dl = self.pq(".action-parameters-table")

        check_payload_dl_order(payloads_dl)
        
        





    def check_toc_with_list(self,toc_elements,list_elements):
        for child in toc_elements:
            try:
                next_element = list_elements.pop(0)
            except IndexError as e:
                print "TOC has to much elements"
                assert False
            except Exception as e:
                print e
                assert False
            link = pq(child).children("a")
            self.assertEqual(pq(link).attr["href"], next_element["href"])
            self.assertEqual(pq(link).text().strip(), next_element["text"].strip())


            if(len(next_element["subelements"])):
                ##recursive
                self.check_toc_with_list(pq(child).children("ul").children(), next_element["subelements"])
                pass

        ##list must be empty
        if (len(list_elements)):
            print "Some TOC elements have benn not appeared"
            print list_elements



def check_parameter_dl_order(parameters_dl):
    for parameter_dl in parameters_dl:
        parameters_name = pq(parameter_dl).find(".parameter-name").text().split(" ")
        
        if not isinstance(parameters_name, basestring):
            assert sorted(parameters_name) == parameters_name

        #check_parameter_dl_order(pq(parameter_dl).find("dl")) #not recursive


def check_payload_dl_order(payloads_dl):
    for payload_dl in payloads_dl:
        payloads_name = pq(payload_dl).children("dt").children(".parameter-name").text().split(" ")
        if not isinstance(payloads_name, basestring):
            assert sorted(payloads_name) == payloads_name


suite = unittest.TestLoader().loadTestsFromTestCase(TestParametersHTML)
unittest.TextTestRunner(verbosity=2).run(suite)