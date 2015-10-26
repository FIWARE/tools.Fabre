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


class TestTOCJSON(unittest.TestCase):
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

        Popen(["fabre", "-i", cls.apib_file, "-o", 
             cls.tmp_result_files, "--no-clear-temp-dir"], stdout=PIPE, stderr=PIPE).communicate()

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


    def test_TOC_HTML(self):

        sel = CSSSelector('nav#toc')

        li_elements=[
            {"text":"FIWARE-NGSI v2 Specification",
            "href":"#API-content",
            "subelements":[]
            },
            {"text":"API Summary",
            "href":"#api-summary",
            "subelements":[]
            },
            {"text":"Specification",
            "href":"#specification",
            "subelements":[
                {"text":"Introduction",
                "href":"#introduction",
                "subelements":[]
                },
            ]
            },
            {"text":"Common Payload Definition",
            "href":"#common-payload-definition",
            "subelements":[]
            },
            {"text":"API Specification",
            "href":"#API_specification",
            "subelements":[
                {"text":"Group Root",
                "href":"#resource_group_root",
                "subelements":[
                    {"text":"GET - Action with attributes and without parent",
                    "href":"#action_action-with-attributes-and-without-parent",
                    "subelements":[]
                    }
                ]
                },
                {"text":"Group Entities",
                "href":"#resource_group_entities",
                "subelements":[
                    {"text":"Resource Resource with attributes",
                    "href":"#resource_resource-with-attributes",
                    "subelements":[
                        {"text":"GET - Action without attr but with resoruce attr",
                        "href":"#action_action-without-attr-but-with-resoruce-attr",
                        "subelements":[]
                        },
                        {"text":"POST - action with attr link",
                        "href":"#action_action-with-attr-link",
                        "subelements":[]
                        }
                    ]
                    },
                    {"text":"Resource Resource with link",
                    "href":"#resource_resource-with-link",
                    "subelements":[
                        {"text":"GET - Action without attr but with resoruce link",
                        "href":"#action_action-without-attr-but-with-resoruce-link",
                        "subelements":[]
                        },
                        {"text":"POST - action with attr link",
                        "href":"#action_action-with-attr-link",
                        "subelements":[]
                        },
                        {"text":"POST - attributes in request test",
                        "href":"#action_attributes-in-request-test",
                        "subelements":[]
                        },
                        {"text":"GET - atributos con recursividad",
                        "href":"#action_atributos-con-recursividad",
                        "subelements":[]
                        },
                    ]

                    }
                ]
                },
                {"text":"Examples",
                "href":"#examples",
                "subelements":[]
                }
            ]
            },
            {
            "text":"Acknowledgements",
            "href":"#acknowledgements",
            "subelements":[]
            }
        ]

        self.check_toc_with_list(self.pq("#toc>ul").children(), li_elements)



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

suite = unittest.TestLoader().loadTestsFromTestCase(TestTOCJSON)
unittest.TextTestRunner(verbosity=2).run(suite)