#!/usr/bin/env python

import unittest
from os import path
import sys


sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from src.drafter_postprocessing.instantiate_uri import instantiate_uri


class TestInstantiatingURIParameters( unittest.TestCase ):
    def test_simple_uri_parameter(self):
        parameters = [
            {
                "name": "id", 
                "example": "32",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{id}', parameters), '/Entity/32')


    def test_simple_empty_uri_parameter(self):
        parameters = [
            {
                "name": "id", 
                "example": "",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{id}', parameters), '/Entity/{id}')


    def test_multiple_simple_uri_parameters(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            },
            {
                "name": "name", 
                "example": "entity-name",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{id}/{name}', parameters), '/Entity/15/entity-name')


    def test_multiple_simple_uri_parameters(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            },
            {
                "name": "name", 
                "example": "entity-name",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{id,name}', parameters), '/Entity/15entity-name')


    def test_hashtag_uri_parameters(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{#id}', parameters), '/Entity/#15')


    def test_empty_hashtag_uri_parameters(self):
        parameters = []
        self.assertEqual(instantiate_uri('/Entity/{#id}', parameters), '/Entity/{#id}')


    def test_form_style_uri_parameter(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity{?id}', parameters), '/Entity?id=15')


    def test_empty_form_style_uri_parameter(self):
        parameters = []
        self.assertEqual(instantiate_uri('/Entity{?id}', parameters), '/Entity')


    def test_multiple_form_style_uri_parameters(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            },
            {
                "name": "name", 
                "example": "entity-name",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{?id,name}', parameters), '/Entity/?id=15&name=entity-name')


    def test_multiple_form_style_uri_parameters_with_empty_ones(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            },
            {
                "name": "name", 
                "example": "",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{?id,name}', parameters), '/Entity/?id=15')


    def test_plus_uri_parameters(self):
        parameters = [
            {
                "name": "resource_path", 
                "example": "path/to/resource",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{+resource_path}', parameters), '/Entity/path/to/resource')


    def test_empty_plus_uri_parameters(self):
        parameters = [
            {
                "name": "resource_path", 
                "example": "",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{+resource_path}', parameters), '/Entity/{+resource_path}')


    def test_multiple_plus_uri_parameters(self):
        parameters = [
            {
                "name": "resource_path_1", 
                "example": "path/to/resource/1",
            },
            {
                "name": "resource_path_2", 
                "example": "",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity/{+resource_path_1,resource_path_2}', parameters), '/Entity/path/to/resource/1{+resource_path_2}')


    def test_ampersand_uri_parameter(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity{&id}', parameters), '/Entity&id=15')


    def test_empty_ampersand_uri_parameter(self):
        parameters = []
        self.assertEqual(instantiate_uri('/Entity{&id}', parameters), '/Entity')


    def test_multiple_ampersand_uri_paramaters(self):
        parameters = [
            {
                "name": "id", 
                "example": "15",
            },
            {
                "name": "name", 
                "example": "entity-name",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity{&id,name}', parameters), '/Entity&id=15&name=entity-name')


    def test_multiple_ampersand_uri_paramaters_with_empty_one(self):
        parameters = [
            {
                "name": "id", 
                "example": "",
            },
            {
                "name": "name", 
                "example": "entity-name",
            }
        ]
        self.assertEqual(instantiate_uri('/Entity{&id,name}', parameters), '/Entity&name=entity-name')


if __name__ == "__main__":
    unittest.main()
