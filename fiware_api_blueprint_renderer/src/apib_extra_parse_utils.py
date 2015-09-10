#!/usr/bin/env python

import json
import re
import sys
import shutil

from pprint import pprint


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

