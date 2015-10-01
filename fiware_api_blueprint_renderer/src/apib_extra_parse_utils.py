#!/usr/bin/env python


import json
import re
import sys
import shutil
from pprint import pprint

import markdown
import mdx_linkify


def parse_to_markdown(markdown_text):
    """Parse Markdown text to HTML

    Arguments:
    markdown_text -- String to be parsed into HTML format
    """

    extensions_list = ['linkify','markdown.extensions.tables','markdown.extensions.fenced_code']

    try:
        parsed_text = markdown.markdown(markdown_text.decode('utf-8'), extensions=extensions_list)

    except (UnicodeEncodeError, UnicodeDecodeError) as encoding_error:
        parsed_text = markdown.markdown(markdown_text, extensions=extensions_list)

    return parsed_text


def get_indentation(line):
    """Returns the indentation (number of spaces and tabs at the begining) of a given line"""
    i = 0
    while (i < len(line) and (line[i] == ' ' or line[i] == '\t')):
        i += 1
    return i


def get_parameter_value_list(file_descriptor, param_regex):

	member_regex = re.compile("^[ \t]*[+|-][ ]([^ +-]*)[ ]*-?(.*)$")

	line = file_descriptor.readline()
	
	value_list = []
	while (line and line.strip(' \n') and not param_regex.match(line)):

		member_match = member_regex.match(line)
		if member_match:
			value_list.append({"name":member_match.group(1), "description":member_match.group(2)})
		
		
		line = file_descriptor.readline()

		while (line.strip(' \n\t') 
			and not line.startswith('+')
			and not line.startswith('-')
			and not line.startswith('#')
			and not member_regex.match(line)
			and not param_regex.match(line)
		):
			value_list[-1]["description"] += line
			line = file_descriptor.readline()


	return (line, value_list)


def get_parameters_with_values(file_descriptor, param_keyword_regex, param_regex, members_keyword_regex):

	member_regex = re.compile("^[ \t]*[+|-][ ]([^ +-]*)[ ]*-?(.*)$")

	line = file_descriptor.readline()
	
	parameters_with_values = []
	while (line):

		param_match = param_regex.match(line)

		if param_match:
			parameter = param_match.group(1)
			line = file_descriptor.readline()

			if members_keyword_regex.match(line):
				(line, value_list) = get_parameter_value_list(file_descriptor, param_regex)

				if value_list:
					parameters_with_values.append({"name": parameter, "values": value_list})

		else:
			if line.startswith('+') or line.startswith('-') or line.startswith('#'):
				break

			line = file_descriptor.readline()

	return (line, parameters_with_values)


def get_header_nested_parameter_values_description(file_descriptor, header_regex, param_keyword_regex, param_regex, members_keyword_regex):

	line = file_descriptor.readline()
		
	parameter_values = []
	while (line and not header_regex.match(line)):

		param_keyword_match = param_keyword_regex.match(line)

		if param_keyword_match:
			(line, parameter_values) = get_parameters_with_values(file_descriptor, param_keyword_regex, param_regex, members_keyword_regex)
		
			if parameter_values:
				break
		else:
			line = file_descriptor.readline()

	return (line, parameter_values)


def get_nested_parameter_values_description(filename):

	header_regex = re.compile("^(#+)[ ]*(.*)$")
	param_keyword_regex = re.compile("^[+|-][ ]Parameters[ ]*$")
	param_regex = re.compile("^[ \t]*[+|-][ ]([^ \(\)]*)[ ][^\(\)]*\(.*\).*$")
	members_keyword_regex = re.compile("^([^+-]*)[+|-][ ]Members[ ]*$")

	nested_description_list = []
	with open(filename, 'r') as read_file:
		
		line = read_file.readline()
		while line:

			header_match = header_regex.match(line)

			if header_match:
				current_parent = line.strip()

				(line, nested_description) = get_header_nested_parameter_values_description(read_file, header_regex, param_keyword_regex, param_regex, members_keyword_regex)
			
				if nested_description:
					nested_description_list.append({ "parent": current_parent, "parameters": nested_description })
			else: 
				line = read_file.readline()
				
	return nested_description_list	


def parse_property_member_declaration(property_member_declaration_string):
  """ Utility to parse the declaration of a property member into custom JSON. Based on the MSON specification. """
  

  # Store MSON reserved words for the parsing below.
  # We are interested in the type attribute reserved keywords in order to know whether 
  # a property member is required or optional.
  reserved_keywords = {}
  reserved_keywords['type_attribute'] = ['required', 'optional', 'fixed', 'sample', 'default']

  if property_member_declaration_string == '': return {}

  # Parse the line in order to get the following fields:
  #  - property_name: The name given to the property
  #  - type_definition_list: The list with the technical definition of the property. Since this
  #    list is unordered, we will parse it later to find the needed keywords.
  #  - description: The text provided to describe the context of the property.
  regex_string = "^[ ]*[-|+][ ](?P<property_name>\w+)[ ]*(?:[[: ][\w, ]*]?[ ]*\((?P<type_definition_list>[\w\W ]+)\))?[ ]*(?:[-](?P<property_description>[ \w\W]+))?\Z"
  declaration_regex = re.compile(regex_string)

  declaration_match = declaration_regex.match(property_member_declaration_string)
  declaration_dict = declaration_match.groupdict()
  
  property_declaration={}
  property_declaration['name'] = declaration_dict['property_name']
  property_declaration['description'] = declaration_dict['property_description']
  property_declaration['subproperties'] = []
  property_declaration['values'] = []

  # Construct the type_definition field from the type_definition_list field retrieved in the
  # regular expression.
  property_declaration['required']=False      # Default value for the required attribute
  for type_specification_attribute in declaration_dict['type_definition_list'].split(','):
    # If the current element is not in the type_attributes reserved keywords list, it is
    # the property type specification.
    if type_specification_attribute.strip() not in reserved_keywords['type_attribute']:
      property_declaration['type'] = type_specification_attribute.strip()
    else:
      if type_specification_attribute.strip() == 'required': property_declaration['required']=True

  return property_declaration


def escape_parenthesis_in_parameter_description(parameter_definition):
    """Given an APIB parameter definition, escape the parenthesis in its description
    
    Arguments:
    line - string containing the parameter definition.
    """


    parameter_definition_list = parameter_definition.split(' - ', 1)
    if len(parameter_definition_list) > 1:
        parameter_header = parameter_definition_list[0]
        parameter_body = parameter_definition_list[1]
        parameter_body = parse_to_markdown(parameter_body)+ '\n'
        parameter_body = parameter_body.replace('<p>', "")
        parameter_body = parameter_body.replace('</p>', "")
        parameter_body = parameter_body.replace('(', "&#40;")
        parameter_body = parameter_body.replace(')', "&#41;")

        return parameter_header + ' - ' + parameter_body
    else:
        return parameter_definition


def preprocess_apib_parameters_lines(line, defining_parameters, defining_data_structure):
    """Preprocess a given APIB line if it contains a parameter definition

    Arguments:
    line - line to be preprocessed
    defining_parameters - bool indicating whether we are in a parameters section (APIB) or not
    defining_data_structure - int indicating the level we are respecting to data strucutres section
    """
    regex_parameter = r"^[ \t]*[+|-][ ]([^ +-]*)[ ]*-?(.*)$"

    if defining_data_structure == 0:
        match_result = re.match(r"^(#*)[ ]Data Structures[ ]*$", line)
        if match_result:
            defining_data_structure = len(match_result.group(0))
            return (line, defining_parameters, defining_data_structure)

    if defining_data_structure > 0:
        if re.match(regex_parameter, line) or re.match(r"^ *$", line):
            line = escape_parenthesis_in_parameter_description(line)
        else:
            match_result = re.match(r"^(#*)[ ].*$", line)
            if match_result:
                if len(match_result.group(0)) <= defining_data_structure:
                    # Stop searching for data structures
                    defining_data_structure = -1

        return (line, defining_parameters, defining_data_structure)

    if not defining_parameters:
        if line == '+ Parameters\n':
            defining_parameters = True
    else:
        if re.match(regex_parameter, line) or re.match(r"^ *$", line):
            line = escape_parenthesis_in_parameter_description(line)
        else:
            if (re.match(r"^[ \t]*[+|-][ ](Attributes)(.*)$", line) or
                re.match(r"^[ \t]*[+|-][ ](Request)(.*)$", line) or
                re.match(r"^[ \t]*[+|-][ ](Response)(.*)$", line) or
                re.match(r"^[ \t]*#(.*)$", line)
                ):
                defining_parameters = False

    return (line, defining_parameters, defining_data_structure)


def start_apib_section(line):
    """Tells if the line indicates the beginning of the apib section.

    Arguments:
    line -- Last read line from the FIWARE extended APIB file.
    """
    result = False

    group_regex = re.compile("^#*[ ]Group([ \w\W\-\_]*)$")
    resource_regex = re.compile("^#*[ ]([ \w\W\-\_]*) \[([ \w\W\-\_]*)\]$")
    direct_URI_regex = re.compile("^#*[ ]([ ]*[/][ \w\W\-\_]*)$")


    if (line.strip() == "# REST API" 
        or line.strip() == "## Data Structures"
        or group_regex.match(line)
        or resource_regex.match(line)
        or direct_URI_regex.match(line)
        ):

        result = True
    
    return result