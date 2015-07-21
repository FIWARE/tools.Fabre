#!/usr/bin/python2

def separate_extra_sections_and_api_blueprint( inputFilePath, extraSectionsFilePath, APIBlueprintFilePath ):
    """Divides a Fiware API specification into extra sections and its API blueprint.

    Arguments:
    inputFilePath -- A Fiware API specification file.
    extraSectionsFilePath -- Resulting file containing extra information about the API specification.
    APIBlueprintFilePath -- Resulting file containing the API blueprint of the Fiware API.
    """
    with open( inputFilePath, 'r' ) as inputFilePath, open( extraSectionsFilePath, 'w') as extraSectionsFile, open( APIBlueprintFilePath, 'w' ) as APIBlueprintFile:
        copy = False
        for line in inputFilePath:
            if line.strip() == "## Editors":
                copy = True
            elif line.strip() == "## Data Structures":
                copy = False

            if copy:
                extraSectionsFile.write( line )
            else:
                APIBlueprintFile.write( line )


def parser_api_blueprint( APIBlueprintFilePath, APIBlueprintJSONFilePath ):
    """Extracts from API Blueprint file the API specification and saves it to a JSON file

    Arguments:
    APIBlueprintFilePath -- An API Blueprint definition file 
    APIBlueprintJSONFilePath -- Path to JSON file
    """
    from subprocess import call

    call( ["drafter", APIBlueprintFilePath, "--output", APIBlueprintJSONFilePath, "--format", "json", "--use-line-num"] )


def get_section_body_from_markdown( markdownFilePath, sectionTitle ):
    """Returns the section body from a Markdown given its title
    
    Arguments:
    markdownFilePath -- A Markdown file  
    sectionTitle -- The section title
    """
    sectionText = ""
    with open( markdownFilePath, 'r' ) as markdownFile:
        line = markdownFile.readline()
        while( ( line != "" ) and ( line != ( sectionTitle + "\n" ) ) ):
            line = markdownFile.readline()

        line = markdownFile.readline()
        while( ( line != "" ) and ( not line.startswith( "#" ) ) ):
            sectionText += line
            line = markdownFile.readline()

    return sectionText


def get_markdow_title_id( sectionTitle ):
    """Returns the HTML equivalent id from a section title
    
    Arguments: 
    sectionTitle -- Section title
    """
    return sectionTitle.lstrip( '#' ).strip().lower()


def parse_meta_data( markdownFilePath ):
    """Parses API metadata and returns the result in a JSON object
    
    Arguments: 
    markdownFilePath -- A Markdown file 
    """
    metadata = {}
    import markdown

    # Extract text sections
    textSectionsHeaders = [ "## Editors", "## Contributors", "## Versions", "## Acknowledgements", "## Status", "## Conformance", "# Specification", "## Introduction", "## Terminology", "## Concepts" ] 
    for textSectionHeader in textSectionsHeaders:
        metadata[ get_markdow_title_id( textSectionHeader ) ] = markdown.markdown( get_section_body_from_markdown( markdownFilePath, textSectionHeader ).decode( "utf-8" ) )

    return metadata


def add_metadata_to_json( metadata, jsonFilePath ):
    """Adds metadata values to a json file
    
    Arguments: 
    metadata -- Metadata values in JSON format
    jsonFilePath -- Path to JSON file
    """
    import json

    jsonContent = ""

    with open( jsonFilePath, 'r' ) as jsonFile:
        jsonContent = json.load( jsonFile )
        jsonContent['api_metadata'] = {}
        for metadataKey in metadata:
            jsonContent['api_metadata'][metadataKey] = metadata[metadataKey]

    with open( jsonFilePath, 'w' ) as jsonFile:
        json.dump( jsonContent, jsonFile, indent=4 )


def parser_json_descriptions_markdown( jsonFilePath ):
    """Gets the descriptions of the resources and parses them as markdown. Saves the result in the same JSON file.
    
    Arguments: 
    jsonFilePath -- Path to JSON file
    """
    import json
    import markdown
    
    jsonContent = ""
    
    with open( jsonFilePath, 'r' ) as jsonFile:
        jsonContent = json.load( jsonFile )
        for resourceGroup in jsonContent['resourceGroups']:
            for resource in resourceGroup['resources']:
                resource['description'] = markdown.markdown( resource['description'] )
    
    with open( jsonFilePath, 'w' ) as jsonFile:
        json.dump( jsonContent, jsonFile, indent=4 )

def copy_static_files( templateDirPath, dstDirPath ):

    import os, shutil

    if os.path.exists(dstDirPath+"/css"):
        shutil.rmtree(dstDirPath+"/css")
    shutil.copytree(templateDirPath+"/css", dstDirPath+"/css")

    if os.path.exists(dstDirPath+"/js"):
        shutil.rmtree(dstDirPath+"/js")
    shutil.copytree(templateDirPath+"/js", dstDirPath+"/js")




def render_api_blueprint( templateFilePath, contextFilePath, dstDirPath ):
    """Renders an API Blueprint context file with a Jinja2 template.
    
    Arguments: 
    templateFilePath -- The Jinja2 template path 
    contextFilePath -- Path to the context file  
    dstDirPath -- Path to save the compiled site
    """
    from jinja2 import Environment, FileSystemLoader
    import json
    import os

    env = Environment( loader=FileSystemLoader( os.path.dirname( templateFilePath ) ) )
    template = env.get_template( os.path.basename( templateFilePath ) )
    output = ""
    with open( contextFilePath, "r" ) as contextFile:
        output = template.render( json.load( contextFile ) )

    renderedHTMLFilename = os.path.splitext( os.path.basename( contextFilePath ) )[0]
    renderedHTMLPath = os.path.join( dstDirPath, renderedHTMLFilename + ".html" )
    with open( renderedHTMLPath, "w" ) as outputFile:
        outputFile.write( output.encode('utf-8') )

    copy_static_files( os.path.dirname(templateFilePath), dstDirPath )


def create_directory_if_not_exists( dirPath ):
    """Creates a directory with the given path if it doesn't exists yet"""
    import os
    if not os.path.exists( dirPath ):
        os.makedirs( dirPath )


def clear_directory( dirPath ):
    """Removes all the files on a directory given its path"""
    import os
    for file in os.listdir( dirPath ):
        filePath = os.path.join( dirPath, file )
        try:
            if os.path.isfile( filePath ):
                os.unlink( filePath )
        except Exception, e:
            print e
    

def render_api_specification( APISpecificationPath, templatePath, dstDirPath, clearTemporalDir = True ):
    """Renders an API specification using a template and saves it to destination directory.
    
    Arguments: 
    APISpecificationPath -- Path to API Blueprint specification
    templatePath -- The Jinja2 template path
    dstDirPath -- Path to save the compiled site
    clearTemporalDir -- Flag to clear temporary files generated by the script  
    """
    import os

    tempDirPath = "/var/tmp/fiware_api_blueprint_renderer_tmp"

    APISpecificationFileName = os.path.splitext( os.path.basename( APISpecificationPath ) )[0]

    APIExtraSectionsFilePath = os.path.join( tempDirPath, APISpecificationFileName + '.extras' )
    APIBlueprintFilePath = os.path.join( tempDirPath + '/' + APISpecificationFileName + '.apib' )
    APIBlueprintJSONFilePath = os.path.join( tempDirPath + '/' + APISpecificationFileName + '.json' )
    
    create_directory_if_not_exists( tempDirPath )
    separate_extra_sections_and_api_blueprint( APISpecificationPath, APIExtraSectionsFilePath, APIBlueprintFilePath )
    parser_api_blueprint( APIBlueprintFilePath, APIBlueprintJSONFilePath )
    add_metadata_to_json( parse_meta_data( APIExtraSectionsFilePath ), APIBlueprintJSONFilePath )
    parser_json_descriptions_markdown( APIBlueprintJSONFilePath )
    render_api_blueprint( templatePath, APIBlueprintJSONFilePath, dstDirPath )
    if( clearTemporalDir == True ):
        clear_directory( tempDirPath )


def main():   
    import sys, inspect, os
    if( len( sys.argv ) < 3 or len( sys.argv ) > 4 ):
        print "ERROR: This script expects 2 / 3 arguments"
        print "Usage: \n\t" + sys.argv[0] + " <api-spec-path> <dst-dir> [clear-temp-dir]"
        sys.exit(-1)

    default_theme = os.path.dirname(__file__)+"/themes/default_theme/api-specification.tpl"

    create_directory_if_not_exists( sys.argv[2] )

    render_api_specification( sys.argv[1], default_theme, sys.argv[2], ( len( sys.argv ) != 4 or ( sys.argv[3] ) ) )
    sys.exit(0)


if __name__ == "__main__":
    main()


