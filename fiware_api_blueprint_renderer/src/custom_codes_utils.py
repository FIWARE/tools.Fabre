#!/usr/bin/env python

import json
import re
import sys
import shutil

from pprint import pprint
import pypandoc


def is_custom_codespec(name):
	"""Return boolean specifying if the input name corresponds with a custom response reserved keyword."""


	custom_codes_list = [
		'response_codes',
		'response_codes_error',
		'response_error_codes'
	]
	if name.lower() in custom_codes_list:
		return True
	else:
		return False

def build_line(string_dict):
	"""Build a string line from Pandoc AST tree structures."""
	
	if string_dict["t"] != 'Plain':
		pprint(string_dict)
		raise ValueError("Unexpected tokenized string structure.")

	string = ''
	for token in string_dict["c"]:
		#pprint(token["c"])
		if token['c']:
			try:
				string += token['c']
			except TypeError:
				# When this object is found, an inline code token has been read
				if token['c'][0] == [u'', [], []]:
					string += '`'+token['c'][1]+ '`'
		else:
			string += ' '

	return string

def get_custom_codes(custom_codes_structure):
	
	try:
		if not is_custom_codespec(custom_codes_structure[0]["c"][0]["c"]):
			raise ValueError("Unexpected custom codes structure.")
	except Exception as e:
		pprint(custom_codes_structure)
		print sys.exc_info()[0]
		raise e

	codes_list = []	
	for string_dict in custom_codes_structure[1]["c"][0]:
		line = build_line(string_dict)

		code_dict = {}

		code_dict["code"] = line.split('-')[0].strip()
		code_dict["comment"] = line.split('-')[1].strip()

		codes_list.append(code_dict)

	return codes_list

def extract_custom_response_section(bullet_list_AST):

	try:
		if bullet_list_AST["t"] != 'BulletList':
			raise ValueError("Unexpected type for BulletList structure.")
	except Exception as e:
		pprint(bullet_list_AST)
		print sys.exc_info()[0]
		raise e 

	codes_list = []
	for element in bullet_list_AST["c"]:
		if element[0]["t"] == 'Plain':
			if is_custom_codespec(element[0]["c"][0]["c"]):
				subCodescodes_list = get_custom_codes(element)

				codes_list += subCodescodes_list

	return codes_list




def extract_values_list(members_list_AST):

	try:
		if members_list_AST["t"] != 'BulletList':
			raise ValueError("Unexpected type for members structure[1].")

		if len(members_list_AST["c"][0]) != 2:
			raise ValueError("Unexpected type for members structure[2].")
			
		if members_list_AST["c"][0][0]["t"] != 'Plain': 
			raise ValueError("Unexpected type for members structure[3].")
		
		if members_list_AST["c"][0][0]["c"][0]["c"] != 'Members':
			raise ValueError("Unexpected type for members structure[4].")

		if members_list_AST["c"][0][1]["t"] != 'BulletList':
			raise ValueError("Unexpected type for members structure[5].")

	except:
		pprint(members_list_AST)
		print sys.exc_info()[0]
		raise 

	values = []

	for member in members_list_AST["c"][0][1]["c"][0]:
		member_line = build_line(member)
		member_value = member_line.split('-')[0].strip()

		member_description = ''
		if len(member_line.split('-'))>1:
			member_description = member_line.split('-')[1].strip()

		values.append({"name": member_value, "description": member_description})

	return values


def extract_values_from_parameter(parameter_AST):

	if len(parameter_AST) == 1:
		return []

	parameter_name = parameter_AST[0]["c"][0]["c"]
	values = extract_values_list(parameter_AST[1])

	return values


def extract_parameters_with_values(parameters_list_content_AST):
	
	parameters_with_values = []
	for parameter in parameters_list_content_AST:
		values = extract_values_from_parameter( parameter )

		if values:
			parameter_name = parameter[0]["c"][0]["c"]
			parameters_with_values.append({"name": parameter_name, "values": values})

	return parameters_with_values

def extract_nested_parameter_values_description(bullet_list_AST):

	try:
		if bullet_list_AST["t"] != 'BulletList':
			raise ValueError("Unexpected type for BulletList structure.")
	except Exception as e:
		pprint(bullet_list_AST)
		print sys.exc_info()[0]
		raise e

	# Check if the BulletList is a Parameters section
	parameters_block = []
	if len(bullet_list_AST["c"])==1:
		if len(bullet_list_AST["c"][0]) == 2:
			AST_block = bullet_list_AST["c"][0]
			if (AST_block[0]["t"] == 'Plain' 
				and AST_block[0]["c"][0]["c"] == 'Parameters'
			):
				parameters_block = AST_block

	# Parameters code block was not found																		
	if not parameters_block:
		return []
	
	
	#pprint( parameters_block )

	parameters_with_values = extract_parameters_with_values(parameters_block[1]["c"])

	#pprint(parameters_with_values)

	return parameters_with_values

def extract_header(header_AST):

	if header_AST["t"] != 'Header':
		pprint(header_AST)
		raise ValueError("Unexpected type for Header structure.")

	headerText=''
	for i in range(header_AST["c"][0]):
		headerText += "#"

	headerText += ' ' + build_line({"t": "Plain", "c": header_AST["c"][2]})

	return headerText


def get_custom_response_codes_from_file(filename):
	
	json_string = pypandoc.convert( filename, format='markdown', to='json' )
	json_obj = json.loads(json_string)

	header_and_bullet_lists = []
	for x in json_obj[1]:
		if "t" in x:
			if x["t"]=='Header':
				header_and_bullet_lists.append(x)
			if x["t"]=='BulletList':
				header_and_bullet_lists.append(x)


	current_parent = {}
	custom_codes_section_list = []
	for element in header_and_bullet_lists:
		if element['t']=='Header':
			current_parent = element
		else:
			custom_codes = extract_custom_response_section(element)
			if custom_codes:
				custom_codes_section_list.append({ "parent": extract_header(current_parent), "custom_codes": custom_codes })


	return custom_codes_section_list


def get_nested_parameter_values_description(filename):
	
	json_string = pypandoc.convert( filename, format='markdown', to='json' )
	json_obj = json.loads(json_string)

	header_and_bullet_lists = []
	for x in json_obj[1]:
		if "t" in x:
			if x["t"]=='Header':
				header_and_bullet_lists.append(x)
			if x["t"]=='BulletList':
				header_and_bullet_lists.append(x)


	current_parent = {}
	nested_description_list = []
	for element in header_and_bullet_lists:
		if element['t']=='Header':
			current_parent = element
		else:
			nested_description = extract_nested_parameter_values_description(element)
			if nested_description:
				nested_description_list.append({ "parent": extract_header(current_parent), "parameters": nested_description })

	return nested_description_list


def delete_custom_codes_from_section( read_file_descriptor, write_file_descriptor ): 
	
	line = read_file_descriptor.readline()
	while line and not line.startswith('#'):

		if line.startswith('+') or line.startswith('-'):

			if is_custom_codespec( line.split(' ')[1].strip() ):
				# Ignore lines until the end of the custom codes section
				while line and line.strip() != '':
					line = read_file_descriptor.readline()
		
		write_file_descriptor.write(line)

		if not line.startswith('#'):
			line = read_file_descriptor.readline()

	return line



def delete_custom_codes_sections_from_file( filename, custom_codes_list ):
	
	editing_filename = filename+'.processing'
	
	shutil.copyfile(filename, filename+'.bak')

	in_parent_section = False
	delete_line = False
	with open(filename, 'r') as read_file:
		with open(editing_filename, 'w') as write_file:

			line = read_file.readline()
			while line:

				regex_string = "^[+-][ ]*(?P<list_first_word>[^ ]*).*$"
				custom_code_regex = re.compile(regex_string)

				custom_code_match = custom_code_regex.match( line )

				if not custom_code_match:
					write_file.write(line)
				else:
					custom_code_match_dict = custom_code_match.groupdict()

					if is_custom_codespec( custom_code_match_dict["list_first_word"].strip() ):
						# Ignore lines until the end of the custom codes section
						while line and line.strip() != '':
							line = read_file.readline()

					else:
						write_file.write(line)
				
				line = read_file.readline()

	shutil.move(editing_filename, filename)

