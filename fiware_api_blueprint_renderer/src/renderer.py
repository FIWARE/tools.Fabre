#!/usr/bin/env python

from collections import OrderedDict
import inspect
import json
import os
import re
import shutil
import io
from subprocess import call, Popen, PIPE
import sys, getopt
import pkg_resources
import subprocess

from jinja2 import Environment, FileSystemLoader

from drafter_postprocessing.json_processing import postprocess_drafter_json
from apib_extra_parse_utils import preprocess_apib_parameters_lines, start_apib_section, get_indentation


def print_api_spec_title_to_extra_file(input_file_path, extra_sections_file_path):
    """Extracts the title of the API specification and writes it to the extra sections file.

    Arguments:
    input_file_path -- File with the API specification
    extra_sections_file_path -- File where we will write the extra sections
    """
    with open(input_file_path, 'rU') as input_file_path, open(extra_sections_file_path, 'w') as extra_sections_file:
        line = input_file_path.readline()
        while (line != "" and not line.startswith("# ")):
            line = input_file_path.readline()
    
        extra_sections_file.write( line )


def separate_extra_sections_and_api_blueprint(input_file_path, extra_sections_file_path, API_blueprint_file_path):
    """Divides a Fiware API specification into extra sections and its API blueprint.

    Arguments:
    input_file_path -- A Fiware API specification file.
    extra_sections_file_path -- Resulting file containing extra information about the API specification.
    API_blueprint_file_path -- Resulting file containing the API blueprint of the Fiware API.
    """
    print_api_spec_title_to_extra_file(input_file_path, extra_sections_file_path) 

    with open(input_file_path, 'rU') as input_file, open(extra_sections_file_path, 'a') as extra_sections_file, open(API_blueprint_file_path, 'w') as API_blueprint_file:
        
        line_counter = 0
        title_line_end = -1
        apib_line_start = -1

        metadata_section = True
        apib_part = False
        title_section = False
        parameters_section = False
        data_structures_section = 0

        for line in input_file:
            line_counter += 1

            copy = False

            if metadata_section and len(line.split(':')) == 1:
                metadata_section = False
                title_section = True
            
            if metadata_section:
                copy = False
            else:
                if title_section and line.startswith('##'):
                    title_section = False

                if title_section:
                    copy = False

                else:
                    if not apib_part:
                        apib_part = start_apib_section(line)
                        if title_line_end < 0:
                            title_line_end = line_counter
                        
                    if not apib_part:
                        copy = True
                    else:
                        copy = False
                        if apib_line_start < 0:
                            apib_line_start = line_counter

            if copy:
                extra_sections_file.write(line)
            else:
                line = line.replace('\t','    ')
                (line, parameters_section, data_structures_section) = preprocess_apib_parameters_lines(line, 
                                                                                                       parameters_section, 
                                                                                                       data_structures_section)
                API_blueprint_file.write(line)

    return (title_line_end, apib_line_start)


def convert_message_error_lines(drafter_output, title_line_end, apib_line_start):
    """Convert the error lines to match the extended FIWARE APIB file format

    Arguments:
    drafter_output -- Text with drafter postprocessing output
    title_line_end -- Line where the specification title ends
    apib_line_start -- Line where the specification of the API starts
    """

    line_error_regex = re.compile( "line (\d+)," )

    line_error_matches = line_error_regex.findall(drafter_output)
    if line_error_matches:
        line_error_set = set(line_error_matches)
        for line_error in line_error_set:
            if line_error >= apib_line_start:
                line_error_substitute = int(line_error) - title_line_end + apib_line_start
                drafter_output = drafter_output.replace("line {},".format(line_error), "line {},".format(line_error_substitute))

    return drafter_output



def parse_api_blueprint_with_drafter(API_blueprint_file_path, API_blueprint_JSON_file_path, title_line_end, apib_line_start):
    """Parse the API Blueprint file with the API specification and save the output to a JSON file

    Arguments:
    API_blueprint_file_path -- An API Blueprint definition file 
    API_blueprint_JSON_file_path -- Path to JSON file
    title_line_end -- Line where the specification title ends. Needed to reconvert error messages from drafter.
    apib_line_start -- Line where the specification of the API starts. Needed to reconvert error messages from drafter.
    """

    command_call = ["drafter", API_blueprint_file_path, "--output", API_blueprint_JSON_file_path, "--format", "json", "--use-line-num"]
    [_, execution_error_output] = Popen(command_call, stderr=PIPE).communicate()

    print convert_message_error_lines(execution_error_output, title_line_end, apib_line_start)


def generate_metadata_dictionary(metadata_section):
    """Generates a metadata section as a dictionary from a non-dictionary section
    
    Arguments:
    metadata_section -- Source metadata section
    """
    metadata_section_dict = {}
    metadata_section_dict['id'] = metadata_section['id']
    metadata_section_dict['name'] = metadata_section['name']
    metadata_section_dict['body'] = metadata_section['body']
    metadata_section_dict['subsections'] = OrderedDict()

    for subsection in metadata_section['subsections']:
        metadata_section_dict['subsections'][subsection['name']] = generate_metadata_dictionary(subsection)

    return metadata_section_dict


def copy_static_files(template_dir_path, dst_dir_path):
    """Copies the static files used by the resulting rendered site
    
    Arguments:
    template_dir_path -- path to the template directory
    dst_dir_path -- destination directory
    """
    subdirectories = ['/css', '/js', '/img', '/font']

    for subdirectory in subdirectories:
        if os.path.exists(dst_dir_path + subdirectory):
            shutil.rmtree(dst_dir_path + subdirectory)
        shutil.copytree(template_dir_path + subdirectory, dst_dir_path + subdirectory, ignore=shutil.ignore_patterns('*.pyc', '*.py'))


def render_api_blueprint(template_file_path, context_file_path, dst_dir_path):
    """Renders an API Blueprint context file with a Jinja2 template.
    
    Arguments: 
    template_file_path -- The Jinja2 template path 
    context_file_path -- Path to the context file  
    dst_dir_path -- Path to save the compiled site
    """

    env = Environment(extensions=["jinja2.ext.do",], loader=FileSystemLoader(os.path.dirname(template_file_path)))
    env.filters['sort_payload_parameters'] = sort_payload_parameters
    env.filters['contains_common_payload_definitions'] = contains_common_payload_definitions
    template = env.get_template(os.path.basename(template_file_path))
    output = ""
    with open(context_file_path, "rU") as contextFile:
        output = template.render(json.load(contextFile))

    rendered_HTML_filename = os.path.splitext(os.path.basename(context_file_path))[0]
    rendered_HTML_path = os.path.join(dst_dir_path, rendered_HTML_filename + ".html")
    with open(rendered_HTML_path, 'w') as output_file:
        output_file.write(output.encode('utf-8'))
    copy_static_files(os.path.dirname(template_file_path), dst_dir_path)


def create_directory_if_not_exists(dir_path):
    """Creates a directory with the given path if it doesn't exists yet"""

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def clear_directory(dir_path):
    """Removes all the files on a directory given its path"""
    
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


def compare_payload_parameter(paramA, paramB):
    """Returns a boolean indicating whether paramA < paramB (alphabetically)

    Arguments:
    paramA - first operand of the comparison
    paramB - second operand of the comparison"""
    if( paramA['class'] == "property" and 
        paramB['class'] == "property" 
    ):
        if( paramA['content']['name']['literal'] < paramB['content']['name']['literal'] ):
            return -1
        else:
            return 1
    else:
        return 0


def sort_payload_parameters(parameters_list):
    """Jinja2 custom filter for ordering a list of parameters

    Arguments:
    parameters_list - list of payload parameters given by Drafter"""
    return sorted(parameters_list, cmp=compare_payload_parameter)


def contains_common_payload_definitions(data_structures):
    """Jinja2 custom filter for checking if a data structures list contains common payload definitions

    Arguments:
    data_structures - list of data structures"""
    for data_structure in data_structures.itervalues():
        if data_structure['is_common_payload']:
            return True
    return False


def render_api_specification(API_specification_path, template_path, dst_dir_path, clear_temporal_dir=True, cover=None):
    """Renders an API specification using a template and saves it to destination directory.
    
    Arguments: 
    API_specification_path -- Path to API Blueprint specification
    template_path -- The Jinja2 template path
    dst_dir_path -- Path to save the compiled site
    clear_temporal_dir -- Flag to clear temporary files generated by the script  
    """

    temp_dir_path = "/var/tmp/fiware_api_blueprint_renderer_tmp"

    API_specification_file_name = os.path.splitext(os.path.basename(API_specification_path))[0]


    API_extra_sections_file_path = os.path.join(temp_dir_path, API_specification_file_name + '.extras')
    API_blueprint_file_path = os.path.join(temp_dir_path + '/' + API_specification_file_name + '.apib')
    API_blueprint_JSON_file_path = os.path.join(temp_dir_path + '/' + API_specification_file_name + '.json')
    
    create_directory_if_not_exists(temp_dir_path)
    (title_line_end, apib_line_start) = separate_extra_sections_and_api_blueprint(API_specification_path, 
                                                                                  API_extra_sections_file_path, 
                                                                                  API_blueprint_file_path)

    parse_api_blueprint_with_drafter(API_blueprint_file_path, API_blueprint_JSON_file_path, title_line_end, apib_line_start)
    
    is_PDF = cover is not None
    postprocess_drafter_json(API_blueprint_JSON_file_path,API_blueprint_file_path,API_extra_sections_file_path, is_PDF)

    render_api_blueprint(template_path, API_blueprint_JSON_file_path, dst_dir_path)

    if is_PDF: #cover needed for pdf
        cover_json_path = os.path.join( dst_dir_path + '/' + 'cover' + '.json' )
        shutil.move(API_blueprint_JSON_file_path, cover_json_path)
        render_api_blueprint( cover, cover_json_path, dst_dir_path )
        shutil.move(cover_json_path, API_blueprint_JSON_file_path)
        return

    if clear_temporal_dir == True:
        clear_directory( temp_dir_path )


def print_package_dependencies():
    """Print the dependencies of package Fabre"""
    
    print "\n# PIP dependencies\n"
    dependencies_matrix = [["Package", "Required version", "Installed version"]]

    version_regex = re.compile("Version: (.*)")
    for package in pkg_resources.get_distribution("fiware_api_blueprint_renderer").requires():
        package_header = str(package).split('>=')
        package_name = package_header[0]
        package_required_version = ">= " + package_header[1]
        package_installed_info = subprocess.check_output(['pip', 'show', package_name])
        package_installed_version = version_regex.search(package_installed_info).group(1)      

        dependencies_matrix.append([package_name, package_required_version, package_installed_version])

    pretty_print_matrix(dependencies_matrix)

    print "\n\n# System dependencies\n"
    system_dependencies = [('drafter', 'v0.1.9'), ('wkhtmltopdf', '0.12.2.1 (with patched qt)')]
    for (package_name, package_required_version) in system_dependencies:
        package_installed_version = subprocess.check_output([package_name, '--version'])

        print "Name: "
        print "\t%s\n" % package_name
        print "Required version: "
        print "\t%s\n" % package_required_version
        print "Installed version (%s --version): " % package_name
        for version_line in package_installed_version.split('\n'):
            print "\t%s" % version_line
    print "\n"


def pretty_print_matrix(matrix):
    """Pretty print the given matrix (as a table)"""

    # Retrieve the size of the matrix longest element
    longest_matrix_string_size = 0
    for row in matrix:
        longest_row_string_size = len(max(row, key=len))
        if longest_row_string_size > longest_matrix_string_size:
            longest_matrix_string_size = longest_row_string_size

    # Print the matrix as a table
    row_format = "{:<%i}" % (longest_matrix_string_size + 2)
    row_format = row_format * len(matrix[0])
    for row in matrix:
        print "\t" + row_format.format(*row)


def main():   
    
    usage = "Usage: \n\t" + sys.argv[0] + " -i <api-spec-path> -o <dst-dir> [--pdf] [--no-clear-temp-dir] [--template]"
    version = "fabre " + pkg_resources.require("fiware_api_blueprint_renderer")[0].version
    
    default_theme = os.path.dirname(__file__)+"/../themes/default_theme/api-specification.tpl"
    pdf_template_path= os.path.dirname(__file__)+"/../themes/default_theme/api-specification.tpl"
    cover_template_path= os.path.dirname(__file__)+"/../themes/default_theme/cover.tpl"
    template_path= default_theme
    clear_temporal_dir = True
    API_specification_path = None
    dst_dir_path = None
    temp_pdf_path = "/var/tmp/fiware_api_blueprint_renderer_tmp_pdf/"
    pdf = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hvi:o:ct:",["version","ifile=","odir=","no-clear-temp-dir","template=","pdf","version-dependencies"])
    except getopt.GetoptError:
      print usage
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-v", "--version"):
            print version
            sys.exit()
        elif opt == '--version-dependencies':
            print version
            print_package_dependencies()
            sys.exit()
        elif opt in ("-i", "--input"):
            API_specification_path = arg
        elif opt in ("-o", "--output"):
            dst_dir_path = arg
        elif opt in ("-t", "--template"):
            template_path = arg
        elif opt in ("-c", "--no-clear-temp-dir"):
            clear_temporal_dir = False
        elif opt in ("--pdf"):
            pdf = True
            #if no template is specified, uses the default pdf template
            if not ('-t' in zip(*opts)[0] or '--template' in zip(*opts)[0]):
                template_path = pdf_template_path


    if API_specification_path is None:
        print "API specification file must be specified"
        print usage
        sys.exit(3)

    if dst_dir_path is None:
        print "Destination directory must be specified"
        print usage
        sys.exit(4)

    if pdf:
        create_directory_if_not_exists(temp_pdf_path)
        rendered_HTML_filename = os.path.splitext(os.path.basename(API_specification_path))[0]
        rendered_HTML_path = os.path.join(temp_pdf_path, rendered_HTML_filename + ".html")
        rendered_HTML_cover = os.path.join(temp_pdf_path, "cover" + ".html")

        if ".pdf" not in dst_dir_path:
            create_directory_if_not_exists(dst_dir_path)
            dst_dir_path = os.path.join(dst_dir_path, rendered_HTML_filename + ".pdf")

        render_api_specification(API_specification_path, template_path, temp_pdf_path, clear_temporal_dir, cover_template_path)
        call( ["wkhtmltopdf", '-d', '125', '--page-size','A4', "page", "file://"+rendered_HTML_cover ,"toc" ,"page", "file://"+rendered_HTML_path, '--footer-center', "Page [page]",'--footer-font-size', '8', '--footer-spacing', '3','--run-script', "setInterval(function(){if(document.readyState=='complete') window.status='done';},100)", "--window-status", "done", dst_dir_path ])
    else:
        create_directory_if_not_exists( dst_dir_path )
        render_api_specification( API_specification_path, template_path, dst_dir_path, clear_temporal_dir, None)
    sys.exit(0)


if __name__ == "__main__":
    main()
