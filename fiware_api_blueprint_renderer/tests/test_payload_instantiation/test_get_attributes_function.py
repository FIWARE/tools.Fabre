
import unittest
from os import path
import sys

import_path = path.abspath(__file__)

while path.split(import_path)[1] != 'fiware_api_blueprint_renderer':

    import_path = path.dirname(import_path)

sys.path.append(import_path)

from src.drafter_postprocessing.instantiate_body import  get_attributes 
from tests.test_utils import *


class TestGetAttributesFunction(unittest.TestCase):
    __metaclass__ = TestCaseWithExamplesMetaclass

    @for_examples(
        ([
            {"class":"memberType",
            "content":[
                {
                    "class":"property",
                    "content":{
                        "name":{
                            "literal":"VariableWithValue"
                        },
                        "valueDefinition":{
                            "values":[
                                {
                                    "literal":"value1-1"
                                },
                                {
                                    "literal":"value2-1"
                                },
                            ]
                        }
                    }
                }
            ]
            },
            {"class":"memberType",
            "content":[
                {
                    "class":"property",
                    "content":{
                        "name":{
                            "literal":"VariableWithValue2"
                        },
                        "valueDefinition":{
                            "values":[
                                {
                                    "literal":"value2-1"
                                },
                                {
                                    "literal":"value2-1"
                                },
                            ]
                        }
                    }
                }
            ]
            },
            {"class":"memberType",
            "content":[
                {
                    "class":"property",
                    "content":{
                        "name":{
                            "literal":"VariableWithValue3"
                        },
                        "valueDefinition":{
                            "values":[]
                        },
                        "sections":[
                            {"class":"memberType",
                            "content":[
                                {
                                    "class": "property",
                                    "content":{
                                        "name":{
                                            "literal":"variableWithoutValue3-1"
                                        },
                                        "valueDefinition":{
                                            "values":[]
                                        },
                                        "sections":[]
                                    }
                                },
                                {
                                    "class": "property",
                                    "content":{
                                        "name":{
                                            "literal":"variableWithValue3-2"
                                        },
                                        "valueDefinition":{
                                            "values":[
                                            {
                                            "literal":"values_second_level3"}
                                            ]
                                        },
                                        "sections":[]
                                    }
                                },
                                {
                                    "class": "property",
                                    "content":{
                                        "name":{
                                            "literal":"variableWithValue3-3"
                                        },
                                        "valueDefinition":{
                                            "values":[]
                                        },
                                        "sections":[
                                            {
                                                "class":"memberType",
                                                "content":[
                                                {
                                                    "class": "property",
                                                    "content":{
                                                        "name":{
                                                            "literal":"variableWithValue3-3-3"
                                                        },
                                                        "valueDefinition":{
                                                            "values":[
                                                            {
                                                            "literal":"third_level_value"
                                                            }]
                                                        },
                                                        "sections":[]
                                                   }
                                                }
                                                ]
                                            }

                                        ]
                                    }
                                },
                            ]

                            }

                        ]
                    }
                }
            ]
            }
        ],{'VariableWithValue': 'value1-1','VariableWithValue2': 'value2-1','VariableWithValue3':{"variableWithValue3-2":"values_second_level3","variableWithValue3-3":{"variableWithValue3-3-3":"third_level_value"}}}),
        )
    def test_get_attributes_function(self, input_sections, expected_attributes):
        obtained_attributes = get_attributes(input_sections)
        self.assertEqual(obtained_attributes, expected_attributes)




suite = unittest.TestLoader().loadTestsFromTestCase(TestGetAttributesFunction)
unittest.TextTestRunner(verbosity=2).run(suite)