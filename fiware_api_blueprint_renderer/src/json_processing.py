#!/usr/bin/env python

from collections import deque
import json
import re

from markdown.extensions.toc import slugify

from apib_extra_parse_utils import parse_property_member_declaration, get_nested_parameter_values_description
from apib_extra_parse_utils import parse_to_markdown, get_indentation


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

    link_regex = re.compile( "\[(?P<linkText>[^\(\)\[\]]*)\]\((?P<linkRef>[^\(\)\[\]]*)\)" )
    auto_link_regex = re.compile("\<(?P<linkRef>http[s]?://.*)\>")
    html_link_regex = re.compile("\<a href=\"(?P<linkRef>http[s]?://.*)\"\>(?P<linkText>[^\<]*)\</a>")

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


def get_markdown_links(json_content):
    """Returns a list with all the Markdown links present in a the json representation of a Markdown file."""

    links = []
    # Abstract
    links += get_links_from_description(json_content["description"])

    # API Metadata
    links += get_links_api_metadata(json_content["api_metadata"])

    # API specification
    for resource_group in json_content["resourceGroups"]:
        links += get_links_from_description(resource_group["description"])

        for resource in resource_group["resources"]:
            links += get_links_from_description(resource["description"])

            for action in resource["actions"]:
                links += get_links_from_description(action["description"])

                for example in action["examples"]:
                    for request in example["requests"]:
                        links += get_links_from_description(request["description"])

                    for response in example["responses"]:
                        links += get_links_from_description(response["description"])

    return links


def parse_defined_data_structure_properties(properties_list, remaining_property_lines):
    """Parses the properties definitions of a given data structure given its body

    Arguments:
    properties_list - List where we'll insert new properties to
    remaining_property_lines - Property definition lines pending to be processed
    """
    last_member_indentation = -1

    while len(remaining_property_lines) > 0:
        property_member_declaration = remaining_property_lines[0]
        if property_member_declaration != '':
            # Retrieve the indentation of the current property definition.
            current_member_indentation = get_indentation(property_member_declaration)
            if last_member_indentation == -1:
                last_member_indentation = current_member_indentation
          
            # Process the new property as a child, parent or uncle of the last
            # one processed according to their relative line indentations.
            if current_member_indentation == last_member_indentation:
                parsed_attribute_definition = parse_property_member_declaration(property_member_declaration)
                remaining_property_lines.popleft()
                properties_list.append(parsed_attribute_definition)
            elif current_member_indentation > last_member_indentation:
                parse_defined_data_structure_properties(parsed_attribute_definition['subproperties'], remaining_property_lines)
            else:
                return
        else:
            remaining_property_lines.popleft()
    

def parse_defined_data_structures(data):
  """Retrieves data structures definition from JSON fragment and gives them back as Python dict"""
  data_structure_dict = {}

  try:
    if data["content"][0]["sections"][0]["class"] != u'blockDescription':
        raise ValueError('Unexpected section received.')
  except:
    return data_structure_dict


  for content in data["content"]:
    data_structure = {}
    data_structure_definition = []

    if content["sections"]!=[]:
      data_structure_content = content["sections"][0]["content"]
      parse_defined_data_structure_properties(data_structure_definition, deque(data_structure_content.split('\n')))

    data_structure_name = content["name"]["literal"]
    data_structure["attributes"] = data_structure_definition
    data_structure_dict[data_structure_name] = data_structure

  return data_structure_dict


def order_request_parameters(request_id):
    """Take a request identifier and if it has a URI, order it parameters.

    Arguments:
    request_id -- String that specifies request that is going to be processed
    """
    
    _last_slash_position = request_id.rfind('/')

    if 0 > _last_slash_position:
        return request_id #parameters not found
    
    last_string = request_id[_last_slash_position:]

    if 1 > len(last_string):
        return request_id #request_id ends with /

    
    start_param = last_string.find('?')

    if 0 > start_param:
        return request_id

    parameters = last_string[start_param+1:]
    
    if 1 > len(parameters):
        return request_id

    fragment_pos = parameters.find('#')

    if fragment_pos < 0: #dont have identifier operator
        query_parameters = ('&').join(sorted(parameters.split('&')))
        ordered_request = request_id[0:_last_slash_position]+\
                        last_string[0:start_param+1]+\
                        query_parameters
    else:
        query_parameters = ('&').join(sorted((parameters[:fragment_pos])\
                            .split('&')))
        ordered_request = request_id[0:_last_slash_position]+\
                        last_string[0:start_param+1]+\
                        query_parameters+parameters[fragment_pos:]


    return ordered_request


def order_uri_block(block):
    """Take a variable block of a URI Template and return it ordered.

    Arguments:
    block -- String that specifies the block to be ordered
    """

    if '#' == block[0]: #fragment identifier operator
        return block
    if '+' == block[0]:
        return block #reserved value operator

    if not ('?' == block[0] or '&' == block[0]): #start with name
        return block

    parameters = (',').join(sorted((block[1:]).split(',')))
    
    return ''+block[0]+ parameters 


def order_uri_parameters(URI):
    """Take an URI and order it parameters.

    Arguments:
    URI -- URI to be ordered
    """
    
    _last_slash_position = URI.rfind('/')
    

    if 0 > _last_slash_position:
        return URI #parameters not found
    
    parameters_string = URI[_last_slash_position:]
    if 1 > len(parameters_string):
        return URI #URI ends with /

    parameter_blocks = parameters_string.split('{')

    orderer_blocks = ""
    for parameter_block in parameter_blocks[1:]:
        
        if 0 > parameter_block.find('}'):#close block not found
            return URI

        _close_group_position = parameter_block.find('}')

        ordered_parameters = order_uri_block(parameter_block[0:\
            _close_group_position])
        orderer_blocks += '{'+ordered_parameters+parameter_block[\
        _close_group_position:]

    ordered_URI = URI[0:_last_slash_position]+parameter_blocks[0]+\
                orderer_blocks

    return ordered_URI


def instantiate_uri(URI_template, parameters):
    """Instantiate an URI template from a list of parameters

    Arguments:
    URI_template - URI template to be instanted
    parameters - List of URI parameters used for instantiating
    """
    # Find all the parameter blocks (ie. {var}, {?var1,var2}, etc). 
    regex = re.compile("{([^}]*)}")
    URI_parameters_blocks = re.findall(regex,URI_template)

    # Process every parameter block found in the URI
    for URI_parameter_block in URI_parameters_blocks:
        # Parameters of the form "#var" will be replaced with "#value", so we
        # keep the '#' as a prefix.
        prefix = ''
        if URI_parameter_block[0] == '#':
            prefix = '#'

        # Form-style parameters (ie. ?var, &var) requires a different 
        # substitution, so mark them as special cases for the substitutions
        # loop.
        form_style_query_parameters = False;
        if URI_parameter_block[0] == '?':
            form_style_query_parameters = True;
            first_form_style_query_parameter = True;
        elif URI_parameter_block[0] == '&':
            form_style_query_parameters = True;
            first_form_style_query_parameter = False;

        # If the current parameters blocks startswith '?', '&', etc we
        # remove such prefix for the substitutions loop.
        if prefix == '' and form_style_query_parameters == False and URI_parameter_block[0] != '+':
            URI_parameter_block_replace = URI_parameter_block
        else:
            URI_parameter_block_replace = URI_parameter_block[1:]

        # Start replacing all the parameters inside the parameter blocks one
        # by one.
        for URI_parameter in URI_parameter_block_replace.split(','):
            # Form-style parameters as "?var" will be replaced by 
            # "?var=value", so keep "var=" as a prefix.
            if form_style_query_parameters == True:
                if first_form_style_query_parameter:
                    prefix = "?" + URI_parameter + "="
                    first_form_style_query_parameter = False
                else:
                    prefix = "&" + URI_parameter + "="

            # Search the current URI parameter in the list of parameters 
            # given and replace its name with its example value.
            i = 0
            parameter_definition_found = False
            while i < len(parameters) and not parameter_definition_found:
                if parameters[i]['name'] == URI_parameter and len(parameters[i]['example']) > 0:
                    parameter_definition_found = True
                    URI_parameter_block_replace = URI_parameter_block_replace.replace(URI_parameter, prefix + parameters[i]['example'])
                i += 1

            # If the parameter can not be found or it has not example value,
            # we replace it with "{prefix+var-name}" or simply ignore it 
            # depending on the type of parameter.
            if parameter_definition_found == False:
                if URI_parameter_block[0] != '?' and URI_parameter_block[0] != '&':
                    if URI_parameter_block[0] == '+':
                        prefix = '+'
                    URI_parameter_block_replace = URI_parameter_block_replace.replace(URI_parameter, "{" + prefix + URI_parameter + "}")
                else:
                    URI_parameter_block_replace = URI_parameter_block_replace.replace(URI_parameter, '')

        # Replace the original parameter block with the values of its members
        # omiting the separator character (',').
        URI_parameter_block_replace = URI_parameter_block_replace.replace(',','')
        URI_template = URI_template.replace("{" + URI_parameter_block + "}",URI_parameter_block_replace)

    return URI_template


def combine_uri_parameters(resource_uri_parameters, action_uri_parameters):
    """Combine the URI parameters of the given action and resource

    Combine URI parameters of the current action and resource. In case 
    of a parameter being defined in both the resource and the action, 
    list only that of the action.

    Arguments:
    resource_uri_parameters -- URI parameters of the given resource
    action_uri_parameters -- URI parameters of the given action 
    """
    uri_parameters = []

    # Append to the result list all the URI parameters from the resource 
    # which are not redefined in the action.
    for resource_uri_parameter in resource_uri_parameters:
        parameter_overwritten_in_action = False
        for action_uri_parameter in action_uri_parameters:
            if resource_uri_parameter["name"] == action_uri_parameter["name"]:
                parameter_overwritten_in_action = True

        if not parameter_overwritten_in_action:
            uri_parameters.append(resource_uri_parameter)

    # Append all the parameters from the action to the result list.
    uri_parameters.extend(action_uri_parameters)

    return uri_parameters


def parse_json_description(JSON_element):
    """Search for a 'decription' key in the current object and parse ti as markdown

    Arguments:
    JSON_element -- JSON element to iterate and parse
    """

    if type(JSON_element) is dict:
        for key in JSON_element:
            if key == "description":
                JSON_element[key] = parse_to_markdown(JSON_element[key]).replace("<p>", "").replace("</p>", "")
            else:
                JSON_element[key] = parse_json_description(JSON_element[key])

    elif type(JSON_element) is list:
        for key in range(len(JSON_element)):
            JSON_element[key] = parse_json_description(JSON_element[key])

    return JSON_element


def get_heading_level(heading):
    """Returns the level of a given Markdown heading
    
    Arguments:
    heading -- Markdown title    
    """
    i = 0
    while( i < len(heading) and heading[i] == '#' ):
        i += 1

    return i


def get_subsection_body(filepath, last_position):
    """Reads the given file until a Markdown header is found and returns the bytes read

    Arguments:
    filepath -- Path of the file to iterate over
    position -- Descriptor of the file being read"""

    with open(filepath, 'rU') as file_descriptor:
        body = ''
        previous_pos = last_position
        file_descriptor.seek(previous_pos)
        line = file_descriptor.readline()
        pos = file_descriptor.tell()

        while line and not line.startswith('#'):
            body += line

            previous_pos = pos
            line = file_descriptor.readline()
            pos = file_descriptor.tell()

        return (body, previous_pos)


def parse_metadata_subsections(filepath, parent_section_JSON, last_pos=0):
    """Generates a JSON tree of nested metadata sections

    Arguments:
    filepath -- Name and path of the file to iterate over
    parent_section_JSON -- JSON object representing the current parent section
    last_pos -- Last byte position read in the file 
    """
    
    previous_pos = last_pos
    with open(filepath, 'rU') as file_descriptor:

        file_descriptor.seek(previous_pos)
        line = file_descriptor.readline()
        pos = file_descriptor.tell()

        # EOF case
        if line:
            if line.startswith('#'):

                section_name = line
                (body, previous_pos) = get_subsection_body(filepath, pos)

                section_JSON = create_json_section(section_name, body)
                parent_section_JSON['subsections'].append(section_JSON)

                section_level = get_heading_level(section_name)

                file_descriptor.seek(previous_pos)
                line = file_descriptor.readline()
                pos = file_descriptor.tell()            
                next_section_level = get_heading_level(line)

                if section_level == next_section_level:   # Section sibling
                   previous_pos = parse_metadata_subsections(filepath, parent_section_JSON, last_pos=previous_pos) 
                elif section_level < next_section_level:  # Section child
                   previous_pos = parse_metadata_subsections(filepath, section_JSON, last_pos=previous_pos) 
                else:   # Not related to current section
                    return previous_pos

                file_descriptor.seek(previous_pos)
                next_line = file_descriptor.readline()
                pos = file_descriptor.tell()

                if next_line :
                    next_section_level = get_heading_level(next_line)
                    if section_level == next_section_level:   # Section sibling
                       previous_pos = parse_metadata_subsections(filepath, parent_section_JSON, last_pos=previous_pos)
                    else:   # Not related to current section
                        pass 

    return previous_pos


def get_markdown_title_id(section_title):
    """Returns the HTML equivalent id from a section title
    
    Arguments: 
    section_title -- Section title
    """
    return section_title.replace(" ", "_").lower()


def create_json_section(section_markdown_title, section_body):
    """Creates a JSON
    
    Arguments:
    section_markdown_title -- Markdown title of the section
    section_body -- body of the subsection
    """
    section_title = section_markdown_title.lstrip('#').strip()

    section = {}
    section["id"] = get_markdown_title_id( section_title )
    section["name"] = section_title
    section["body"] = parse_to_markdown(section_body)

    section["subsections"] = []

    return section


def parse_meta_data(filepath):
    """Parses API metadata and returns the result in a JSON object
    
    Arguments: 
    filepath -- File with extra sections
    """
    metadata = create_json_section("root", "")
  
    with open(filepath, 'rU') as file_:
        last_position_read = parse_metadata_subsections(filepath, metadata)

        file_.seek(last_position_read)
        line = file_.readline()
        while(line):
            last_position_read = parse_metadata_subsections(filepath, metadata, last_position_read)
            file_.seek(last_position_read)
            line = file_.readline()

    return metadata


def add_metadata_to_json(metadata, json_content):
    """Adds metadata values to a json object
    
    Arguments: 
    metadata -- Metadata values in JSON format
    json_content -- JSON object
    """
    json_content['api_metadata'] = {}
    for metadataKey in metadata:
        json_content['api_metadata'][metadataKey] = metadata[metadataKey]


def parser_json_descriptions(json_content):
    """Gets the descriptions of resources and actions and parses them as markdown. Saves the result in the same JSON file.
    
    Arguments: 
    json_content -- JSON object containing the parsed apib.
    """
    json_content = parse_json_description(json_content)


def instantiate_request_uri_templates(json_content):
    """Instantiate the parameters for all the requests URI templates

    Arguments:
    json_content -- JSON object containing the API parsed spec
    """
    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:
            for action in resource["actions"]:
                for example in action["examples"]:
                    for request in example["requests"]:
                        if request["name"].find('/') < 0:
                            # URI parameters can be defined in the resource 
                            # and / or the action. Combine the list of parameters
                            # of both.
                            uri_parameters = combine_uri_parameters(resource["parameters"], action["parameters"])
                                
                            # Instantiate the parameters in the action URI (or in
                            # the resource URI if action URI is empty).
                            if len(action["attributes"]["uriTemplate"]) > 0:
                                request["name"] = \
                                    request["name"] + " " + instantiate_uri( action["attributes"]["uriTemplate"], uri_parameters)
                            else:
                                request["name"] = \
                                    request["name"] + " " + instantiate_uri( resource["uriTemplate"], uri_parameters)


def order_uri_template_of_json(json_content):
    """Extract all the links from the JSON object and adds them back to the JSON.

    Arguments:
    json_content -- JSON object whose URI templates will be ordered.
    """
    for resource_group in json_content["resourceGroups"]:

        for resource in resource_group["resources"]:
            resource["uriTemplate"] = order_uri_parameters(resource["uriTemplate"])
            for action in resource["actions"]:
                action["attributes"]["uriTemplate"] = order_uri_parameters(\
                                        action["attributes"]["uriTemplate"])
                for example in action["examples"]:
                    for request in example["requests"]:
                        request["name"] = \
                                order_request_parameters(request["name"])
    return


def parser_json_data_structures(json_content):
    """Retrieves data structures definition from JSON file and writes them in an easier to access format"""
    
    if len(json_content['content']) > 0:
        json_content['data_structures'] = parse_defined_data_structures(json_content['content'][0])
    else:
        json_content['data_structures'] = {}


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


def add_reference_links_to_json(json_content):
    """Extract all the links from the JSON file and adds them back to the JSON.

    Arguments:
    json_content -- JSON object where all the links will be extracted and added in a separate section.
    """
    json_content['reference_links'] = get_markdown_links(json_content)


def postprocess_drafter_json(JSON_file_path, API_blueprint_file_path, API_extra_sections_file_path, is_PDF):
    """Apply a set of modifications to a JSON file containing an API specification""" 
    with open(JSON_file_path, 'rU') as json_file:
        json_content = json.load(json_file)
    
    add_metadata_to_json(parse_meta_data(API_extra_sections_file_path), json_content)
    add_nested_parameter_description_to_json(API_blueprint_file_path, json_content)
    parser_json_descriptions(json_content)
    instantiate_request_uri_templates(json_content)
    order_uri_template_of_json(json_content)####--##
    parser_json_data_structures(json_content)
    find_and_mark_empty_resources(json_content)
    render_description(json_content)
    escape_requests_responses_json(json_content)
    escape_ampersand_uri_templates(json_content)
    generate_resources_and_action_ids(json_content)
    remove_redundant_spaces(json_content)
    add_reference_links_to_json(json_content)

    json_content['is_PDF'] = is_PDF

    with open(JSON_file_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)
