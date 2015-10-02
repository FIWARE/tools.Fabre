#!/usr/bin/env python

import json
import os
import pprint

def instantiate_all_example_body(json_content):
    """Instantiate the body of payload if it is not specified.

    Arguments:
    JSON_content -- JSON with APIB definition
    """
    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:
            for action in resource["actions"]:
                for example in action["examples"]:
                    for request in example["requests"]:
                        if len(request["body"]):
                            continue #if it has body don't replace it

                        ##check itselft definition ???
                        if len(request['content']):
                            for data_structure in request["content"]:
                                if len(data_structure["sections"]):

                                   _json=get_attributes(data_structure["sections"])
                                   if {} == _json:
                                        continue
                                   request["body"] = json.dumps(_json,sort_keys=True, indent=4)
                                else:
                                    try:
                                        _json = get_attributes_from_data_structure(data_structure["typeDefinition"]["typeSpecification"]["name"]["literal"],json_content["data_structures"] )
                                        if {} == _json:
                                            continue
                                        request["body"] = json.dumps(_json, sort_keys=True, indent=4)
                                    except Exception, e:
                                        print "error resquest"
                                        pass
                            continue
                        #check action parent
                        if len(action["content"]): 
                            #it has elements
                            for data_structure in action["content"]:
                                if len(data_structure["sections"]):

                                   request["body"] = json.dumps(get_attributes(data_structure["sections"]),sort_keys=True, indent=4)

                                else:
                                    try:
                                        _json = get_attributes_from_data_structure(data_structure["typeDefinition"]["typeSpecification"]["name"]["literal"],json_content["data_structures"] )
                                        if {} == _json:
                                            continue
                                        request["body"] = json.dumps(_json, sort_keys=True, indent=4)
                                    except Exception, e:
                                        print "error resquest"
                                        pass
                            continue
                        
                        #check resource grandparent
                        if len(resource["content"]):
                            
                            for data_structure in resource["content"]:
                                if len(data_structure["sections"]):


                                   _json = get_attributes(data_structure["sections"])
                                   if {} == _json:
                                        continue
                                   request["body"] = json.dumps(_json, sort_keys=True, indent=4)
                                else:
                                    try:
                                        _json = get_attributes_from_data_structure(data_structure["typeDefinition"]["typeSpecification"]["name"]["literal"],json_content["data_structures"] )
                                        if {} == _json:
                                            continue
                                        request["body"] = json.dumps(_json, sort_keys=True, indent=4)
                                    except Exception, e:
                                        print "error resquest"
                                        pass
                            continue

    return


def get_attributes(sections):

    _json={}
    for section in sections:
        if section["class"] == "memberType":
            for contents in section["content"]:
                if contents["class"] == "property":
                    try:
                        name = contents["content"]["name"]["literal"]
                        value = contents["content"]["valueDefinition"]["values"][0]["literal"] # TODO check if not literal

                        _json[name]=value

                    except Exception, e:
                        try:
                            name = contents["content"]["name"]["literal"]
                            value = get_attributes(contents["content"]["sections"])
                            if value != {}:
                                _json[name]=value

                        except Exception, e:
                            pass
                        pass

    return _json



def get_attributes_from_data_structure(structure_name, data_structures):


    _json={}
    try:
        for attribute in data_structures[structure_name]["attributes"]:
            if len(attribute["values"]):
                #print attribute["name"], " --> ", attribute["values"][0]
                _json[attribute["name"]] = attribute["values"][0]
            else:
                if len (attribute["subproperties"]):
                    _inner_json = {}
                    _inner_json = get_recursive_attributes_from_data_structure(attribute["subproperties"])
                    if {} == _inner_json:
                        continue
                    
                    _json[attribute["name"]] = _inner_json

    except Exception, e:
        print "Data structure "+structure_name+" not found"
        return _json

    return _json
    


def get_recursive_attributes_from_data_structure(subproperties):
    
    _json = {}
    for subproperty in subproperties:
        if len(subproperty['values']):
            _json[subproperty['name']] = subproperty['values'][0]
            continue

        if len(subproperty['subproperties']):
            _inner_json = {}
            _inner_json = get_recursive_attributes_from_data_structure(subproperty['subproperties'])

            if {} == _inner_json:
                continue

            _json[subproperty['name']] = _inner_json

    return _json
