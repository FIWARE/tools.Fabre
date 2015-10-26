
import unittest
from os import path
import sys

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.instantiate_body import get_attributes_from_data_structure 
from tests.test_utils import *

data_structures = {
"structure1":{
    "attributes":[
        {"name": "attributeWithoutValue",
        "values":[],
        "subproperties":[]
        },
        {"name":"attributeWithValue1",
        "values":['value1', 'value2'],
        "subproperties":[]
        },
        {"name":"attributeWithRecursiveValue",
        "values":[],
        "subproperties":[
            {"name": "recursiveWithoutValue",
            "values":[],
            "subproperties":[]
            },
            {"name": "recursiveWithValue1",
            "values":['RecursiveVal1'],
            "subproperties":[]
            },
            {"name": "recursiveWithValueRecursive",
            "values":[],
            "subproperties":[
                {"name":"recursiveThirdLevel1",
                "values":[
                    'value_recursive_third1'],
                    "subproperties":[]

                },
                {"name":"recursiveThirdLevel2",
                "values":[
                    'value_recursive_third2'],
                    "subproperties":[]

                }
            ]
            },
            {"name":"recursiveWithValue2",
            "values":["value_recursive2"],
           "subproperties":[]
            }
        ]
        }
    ]
    },
"structure2":{
    "attributes":[
        {"name":"structure2_var",
        "values":["5"],
        "subproperties":[]
        },
        {"name":"structure2_var2",
        "values":["6","7"],
        "subproperties":[]
        }
    ]
}

}

class TestGetAttributesFromDataStructureFunction(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass

    @for_examples(
        ('structure2',{"structure2_var":"5", "structure2_var2":"6"}),
        ('structure1',{"attributeWithValue1":"value1", "attributeWithRecursiveValue":{"recursiveWithValue1":"RecursiveVal1", "recursiveWithValueRecursive":{"recursiveThirdLevel1":"value_recursive_third1","recursiveThirdLevel2":"value_recursive_third2"},"recursiveWithValue2":"value_recursive2"}})
        )
    def test_get_attributes_function(self, structure_name, expected_attributes):
        obtained_attributes = (
            get_attributes_from_data_structure(structure_name, data_structures) )
        self.assertEqual(obtained_attributes, expected_attributes)




suite = unittest.TestLoader().loadTestsFromTestCase(TestGetAttributesFromDataStructureFunction)
unittest.TextTestRunner(verbosity=2).run(suite)