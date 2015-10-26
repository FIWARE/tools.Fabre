#!/usr/bin/env python

import json
import sys
from os import path
import re

from markdown.extensions.toc import slugify

if __package__ is None:
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from apib_extra_parse_utils import get_nested_parameter_values_description
    from apib_extra_parse_utils import parse_to_markdown
else:
    from ..apib_extra_parse_utils import get_nested_parameter_values_description
    from ..apib_extra_parse_utils import parse_to_markdown

from data_structures import parser_json_data_structures
from instantiate_body import instantiate_all_example_body
from instantiate_uri import instantiate_request_uri_templates
from metadata import parse_meta_data
from order_uri import order_uri_template_of_json


def extract_markdown_header_dict(markdown_header):
    """Returns a dict with the elements of a given Markdown header (for resources or actions)"""
    markdown_header = markdown_header.lstrip('#').strip()
    
    p = re.compile("(.*) \[(\w*) (.*)\]")
    
    header_dict = {}
    if p.match( markdown_header ):
        header_groups = p.match(markdown_header).groups()

        header_dict['name'] = header_groups[0]
        header_dict['method'] = header_groups[1]
        header_dict['uriTemplate'] = header_groups[2]
    else:
        p = re.compile("(.*) \[(.*)\]")
        header_groups = p.match( markdown_header ).groups()

        header_dict['name'] = header_groups[0]
        header_dict['uriTemplate'] = header_groups[1]
        
    return header_dict


def add_nested_parameter_description_to_json(API_blueprint_file_path, json_content):
    """Extracts all nested description for`parameter values and adds them to the JSON.

    Arguments:
    API_specification_path -- path to the specification file where all the links will be extracted from.
    json_content -- JSON object where all the links will be added.
    """
    nested_descriptions_list = get_nested_parameter_values_description(API_blueprint_file_path)

    for nested_description in nested_descriptions_list:
        for parameter in nested_description["parameters"]:
            for value in parameter["values"]:

                add_description_to_json_parameter_value(json_content, 
                                                        nested_description["parent"], 
                                                        parameter["name"],
                                                        value["name"],
                                                        value["description"])


def add_description_to_json_parameter_value(json_content, resource_or_action_markdown_header, parameter_name, value_name, value_description):
    """"""
    wanted_object = extract_markdown_header_dict( resource_or_action_markdown_header)

    found_object = None

    if 'method' in wanted_object:
        for resource_group in json_content['resourceGroups']:
            for resource in resource_group['resources']:
                for action in resource['actions']:
                    if( action['name'] == wanted_object['name'] and action['method'] == wanted_object['method'] and action['attributes']['uriTemplate'] == wanted_object['uriTemplate'] ):
                        found_object = action
                        break
    else:
        for resource_group in json_content['resourceGroups']:
            for resource in resource_group['resources']:
                if resource['name'] == wanted_object['name'] and resource['uriTemplate'] == wanted_object['uriTemplate']:
                    found_object = resource
                    break

    if found_object != None:
        add_description_to_json_object_parameter_value(found_object, parameter_name, value_name, value_description)


def add_description_to_json_object_parameter_value(JSON_object, parameter_name, value_name, value_description):
    """"""
    value_object = None

    for object_parameter in JSON_object['parameters']:
        if object_parameter['name'] == parameter_name:
            for parameter_value in object_parameter['values']:
                if parameter_value['value'] == value_name:
                    value_object = parameter_value
                    
    if value_object != None:
        value_object['description'] = value_description


def get_links_from_description(description):
    """Find via regex all the links in a description string"""

    link_regex = re.compile( r"\[(?P<linkText>[^\(\)\[\]]*)\]\((?P<linkRef>[^\(\)\[\]]*)\)" )
    auto_link_regex = re.compile(r"\<(?P<linkRef>http[s]?://[^\"]*)\>")
    html_link_regex = re.compile(r"\<a href=\"(?P<linkRef>http[s]?://[^\"]*)\"\>(?P<linkText>[^\<]*)\</a>")

    links = []

    link_matches = link_regex.findall(description)
    if link_matches:
        for link_match in link_matches:
            link = {}
            link['title'] = link_match[0]
            link['url'] = link_match[1]

            links.append(link)
    else:
        link_matches = auto_link_regex.findall(description)
        if link_matches:
            for link_match in link_matches:
                link = {}
                link['title'] = link_match
                link['url'] = link_match

                links.append(link)
        else:
            link_matches = html_link_regex.findall(description)
            if link_matches:
                for link_match in link_matches:
                    link = {}
                    link['title'] = link_match[1]
                    link['url'] = link_match[0]

                    links.append(link)

    return links


def get_links_api_metadata(section):
    """Recursively get links from the api_metadata json section."""


    links = []
    links += get_links_from_description(section["body"])

    for subsection in section["subsections"]:
        links += get_links_api_metadata(subsection)

    return links



def parse_json_description(JSON_element, links):
    """Search for a 'decription' key in the current object and parse ti as markdown

    Arguments:
    JSON_element -- JSON element to iterate and parse
    links - List of links gathered from the descriptions
    """

    if type(JSON_element) is dict:
        for key in JSON_element:
            if key == "description":
                JSON_element[key] = parse_to_markdown(JSON_element[key])

                for link in get_links_from_description(JSON_element[key]):
                    if link not in links:
                        links.append(link)
                
            else:
                JSON_element[key] = parse_json_description(JSON_element[key], links)

    elif type(JSON_element) is list:
        for key in range(len(JSON_element)):
            JSON_element[key] = parse_json_description(JSON_element[key], links)

    return JSON_element


def add_metadata_to_json(metadata, json_content):
    """Adds metadata values to a json object
    
    Arguments: 
    metadata -- Metadata values in JSON format
    json_content -- JSON object
    """
    json_content['api_metadata'] = {}
    for metadataKey in metadata:
        json_content['api_metadata'][metadataKey] = metadata[metadataKey]


def parse_json_descriptions_and_get_links(json_content):
    """Gets the descriptions of resources and actions and parses them as markdown. Saves the result in the same JSON file.
    
    Arguments: 
    json_content -- JSON object containing the parsed apib.
    """
    links = []
    # Abstract
    for link in get_links_from_description(json_content["description"]):
        if link not in links: links.append(link)

    # API Metadata
    for link in get_links_api_metadata(json_content["api_metadata"]):
        if link not in links: links.append(link)

    json_content = parse_json_description(json_content, links)

    return links




def find_and_mark_empty_resources(json_content):
    """Makes a resource able to be ignored by emprtying its title. 

    When a resource has only one action and they share names, the APIB declared an action witohut parent resource.
    """
    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:
            if len(resource["actions"]) == 1:
                if resource["actions"][0]["name"] == resource["name"]:
                    resource["ignoreTOC"] = True
                else:
                    resource["ignoreTOC"] = False


def render_description(json_content):
    """Escaping ampersand symbol form URIs.

    Arguments:
    JSON_file_path -- path to the JSON file where the ampersand will be be escaped in URIs.
    """
    json_content["description"] = parse_to_markdown(json_content["description"])


def escape_requests_responses_json(json_content):
    """Identifies when the body of a request or response uses an XML like type and escapes the '<' for browser rendering.

    Arguments:
    json_content -- JSON content where requests and responses with XML like body will be escaped.
    """
    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:
            for action in resource["actions"]:
                for example in action["examples"]:

                    for request in example["requests"]:
                        if request["body"]:
                            request["body"] = request["body"].replace("<", "&lt;")
                            if not "sections" in request["content"][0]:
                                request["content"][0]["content"] = request["content"][0]["content"].replace("<", "&lt;")

                    for response in example["responses"]:
                        if response["body"]:
                            response["body"] = response["body"].replace("<", "&lt;")
                            if not "sections" in response["content"][0]:
                                response["content"][0]["content"] = response["content"][0]["content"].replace("<", "&lt;")


def escape_ampersand_uri_templates(json_content):
    """Renders the description of the API spscification to display it properly.

    Arguments:
    json_content - json object containing the content to be replaced.
    """
    if(isinstance(json_content, dict)):
        for key, value in json_content.iteritems():
            if isinstance(value, dict) or isinstance(value, list):
                escape_ampersand_uri_templates(value)
            elif key == 'uriTemplate':
                json_content[key] = json_content[key].replace('&', '&amp;')
    elif(isinstance(json_content,list)):
        for value in json_content:
            if isinstance(value, dict) or isinstance(value, list):
                escape_ampersand_uri_templates(value)


def generate_resources_and_action_ids(json_content):
    """Generate an ID for every resource and action in the given JSON file

    Arguments:
    json_content - JSON object containing the API parsed definition"""
    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:
            if len( resource["name"] ) > 0:
                resource["id"] = 'resource_' + slugify( resource["name"], '-' )
            else:
                resource["id"] = 'resource_' + slugify( resource["uriTemplate"], '-' )

            for action in resource["actions"]:
                if len( action["name"] ) > 0:
                    action["id"] = 'action_' + slugify( action["name"],'-' )
                else:
                    if len( action["attributes"]["uriTemplate"] ) > 0:
                        action["id"] = 'action_' + slugify( action["attributes"]["uriTemplate"], '-' )
                    else:
                        if resource["ignoreTOC"] == True:
                            action["id"] = 'action_' + slugify( resource["uriTemplate"] + action["method"], '-' )
                        else:
                            action["id"] = 'action_' + slugify( resource["name"] + action["method"], '-' )


def remove_redundant_spaces(json_content):
    """Remove redundant spaces from names of resources and actions

    Arguments:
    json_content - a JSON object containing the API parsed definition"""

    for resource_group in json_content["resourceGroups"]:
        resource_group["name"] = re.sub( " +", " ", resource_group["name"] )
        for resource in resource_group["resources"]:
            resource["name"] = re.sub( " +", " ", resource["name"] )
            for action in resource["actions"]:
                action["name"] = re.sub( " +", " ", action["name"] )



def postprocess_drafter_json(JSON_file_path, API_blueprint_file_path, API_extra_sections_file_path, is_PDF):
    """Apply a set of modifications to a JSON file containing an API specification""" 
    with open(JSON_file_path, 'rU') as json_file:
        json_content = json.load(json_file)
    
    add_metadata_to_json(parse_meta_data(API_extra_sections_file_path), json_content)
    add_nested_parameter_description_to_json(API_blueprint_file_path, json_content)
    links = parse_json_descriptions_and_get_links(json_content)
    json_content['reference_links'] = links
    instantiate_request_uri_templates(json_content)
    order_uri_template_of_json(json_content)####--##
    parser_json_data_structures(json_content)
    find_and_mark_empty_resources(json_content)
    render_description(json_content)
    escape_requests_responses_json(json_content)
    escape_ampersand_uri_templates(json_content)
    generate_resources_and_action_ids(json_content)
    remove_redundant_spaces(json_content)
    instantiate_all_example_body(json_content)##

    json_content['is_PDF'] = is_PDF

    with open(JSON_file_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)
