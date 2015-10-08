from collections import deque

from ..apib_extra_parse_utils import parse_property_member_declaration
from ..apib_extra_parse_utils import get_indentation

def parser_json_data_structures(json_content):
    """Retrieves data structures definition from JSON file and writes them in an easier to access format"""
    
    if len(json_content['content']) > 0:
        json_content['data_structures'] = parse_defined_data_structures(json_content['content'][0])
    else:
        json_content['data_structures'] = {}


    # Add resource level defined data structures
    structures_from_resources = get_data_structures_from_resources(json_content)
    json_content['data_structures'].update(structures_from_resources)


def get_data_structures_from_resources(json_content):
    """Retrieve data structures defined in named resources.

    Arguments:
    json_content -- JSON object where resources will be analysed
    """

    data_structures = {}

    for resource_group in json_content["resourceGroups"]:
        for resource in resource_group["resources"]:

            if resource["name"] == "": continue

            for content in resource["content"]:
                if content["element"] == "dataStructure":
                    # Retrieve it if it is not a link to another data structure
                    if content["typeDefinition"]["typeSpecification"]["name"] == 'object':  
                        attributes = get_data_structure_properties_from_json(content["sections"])
                        data_structures[resource["name"]] = {"attributes": attributes, "is_common_payload": False}


    return data_structures


def get_data_structure_properties_from_json(data_structure_content):
    """Extract simpler representation of properties from drafter JSON representation.

    Arguments:
    data_structure_content -- JSON content section of "dataStructures" element or nested property
    """
    attributes = []

    for membertype in data_structure_content:
        if "content" not in membertype: return attributes
        
        for property_ in membertype["content"]:
            attribute = {}

            attribute['name'] = property_['content']['name']['literal']
            attribute['required'] = 'required' in property_['content']['valueDefinition']['typeDefinition']['attributes']
            attribute['type'] = \
                property_['content']['valueDefinition']['typeDefinition']['typeSpecification']['name']
            attribute['description'] = property_['content']['description']
            try:
                values_string = property_['content']['valueDefinition']['values'][0]['literal']
                attribute['values'] = [e.strip(" ") for e in values_string.split(',')]
            except IndexError as error:
                attribute['values'] = []
            attribute['subproperties'] = get_data_structure_properties_from_json(property_['content']["sections"])

            attributes.append(attribute)

    return attributes


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
    data_structure["is_common_payload"] = True
    data_structure_dict[data_structure_name] = data_structure

  return data_structure_dict


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