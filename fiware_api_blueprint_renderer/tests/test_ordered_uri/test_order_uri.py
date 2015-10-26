
import unittest
from os import path
import sys

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.order_uri import  order_uri_parameters, order_request_parameters
from tests.test_utils import *


class TestOrderURIFunctions(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass

    @for_examples(
        ('api/entity/v2', 'api/entity/v2'),
        ('api/entity/', 'api/entity/'),
        ('api/entity/v2?get=2&opt=test', 'api/entity/v2?get=2&opt=test'),
        ('api/entity/v2?opt=test&get=2', 'api/entity/v2?get=2&opt=test'),
        ('api/entity/?get=2&opt=test', 'api/entity/?get=2&opt=test'),
        ('api/entity/?opt=test&get=2', 'api/entity/?get=2&opt=test'),
        ('api/entity/v2?get=2&opt=test#anchor', 'api/entity/v2?get=2&opt=test#anchor'),
        ('api/entity/v2?opt=test&get=2#anchor', 'api/entity/v2?get=2&opt=test#anchor'),
        ('api/entity/?get=2&opt=test#anchor', 'api/entity/?get=2&opt=test#anchor'),
        ('api/entity/?opt=test&get=2#anchor', 'api/entity/?get=2&opt=test#anchor'),
        )
    def test_order_request_parameters_function(self, original_request, expected_request):
        
        converted_request = order_request_parameters(original_request)
        self.assertEqual(converted_request, expected_request)

    @for_examples(
        ('api/entity/v2', 
            'api/entity/v2'),

        ('api/entity/', 
            'api/entity/'),

        ('/path/{+var}/42', 
            '/path/{+var}/42'),

        ('/path/to/resources/{varone}{?vartwo}', 
            '/path/to/resources/{varone}{?vartwo}'),

        ('/path/to/resources/{varone}?path=test{&vartwo,varthree}', 
            '/path/to/resources/{varone}?path=test{&varthree,vartwo}'),

        ('/path/to/resources/{varone}?path=test{&varthree,vartwo}', 
            '/path/to/resources/{varone}?path=test{&varthree,vartwo}'),

        ('/path/to/resources/{varone}{?vartwo,varthree}', 
            '/path/to/resources/{varone}{?varthree,vartwo}'),

        ('/path/to/resources/{varone}{?varthree,vartwo}', 
            '/path/to/resources/{varone}{?varthree,vartwo}'),

        ('/path/to/resources/{varone}{?varthree,vartwo}{&varfour,varfive}', 
            '/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}'),
        
        ('/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}', 
            '/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}'),
        
        ('api/entity/v2#anchor', 
            'api/entity/v2#anchor'),

        ('api/entity/#anchor', 
            'api/entity/#anchor'),

        ('/path/{+var}/42#anchor', 
            '/path/{+var}/42#anchor'),

        ('/path/to/resources/{varone}{?vartwo}#anchor', 
            '/path/to/resources/{varone}{?vartwo}#anchor'),

        ('/path/to/resources/{varone}?path=test{&vartwo,varthree}#anchor', 
            '/path/to/resources/{varone}?path=test{&varthree,vartwo}#anchor'),

        ('/path/to/resources/{varone}?path=test{&varthree,vartwo}#anchor', 
            '/path/to/resources/{varone}?path=test{&varthree,vartwo}#anchor'),

        ('/path/to/resources/{varone}{?vartwo,varthree}#anchor', 
            '/path/to/resources/{varone}{?varthree,vartwo}#anchor'),

        ('/path/to/resources/{varone}{?varthree,vartwo}#anchor', 
            '/path/to/resources/{varone}{?varthree,vartwo}#anchor'),

        ('/path/to/resources/{varone}{?varthree,vartwo}{&varfour,varfive}#anchor', 
            '/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}#anchor'),

        ('/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}#anchor', 
            '/path/to/resources/{varone}{?varthree,vartwo}{&varfive,varfour}#anchor'),
        )
    def test_order_uri_parameters_functions(self, original_uri, expected_uri):

        converted_uri = order_uri_parameters(original_uri)
        self.assertEqual(converted_uri,expected_uri)




suite = unittest.TestLoader().loadTestsFromTestCase(TestOrderURIFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)