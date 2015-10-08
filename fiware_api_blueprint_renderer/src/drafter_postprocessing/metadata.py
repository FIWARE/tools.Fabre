from ..apib_extra_parse_utils import parse_to_markdown

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


def get_markdown_title_id(section_title):
    """Returns the HTML equivalent id from a section title
    
    Arguments: 
    section_title -- Section title
    """
    return section_title.replace(" ", "_").lower()


def get_heading_level(heading):
    """Returns the level of a given Markdown heading
    
    Arguments:
    heading -- Markdown title    
    """
    i = 0
    while( i < len(heading) and heading[i] == '#' ):
        i += 1

    return i