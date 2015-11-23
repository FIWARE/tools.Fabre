import re

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
                        if request["name"].replace(' ', '').replace('\t', '').lower().startswith('example-'):
                            request["is_example"] = True
                        else:
                            request["is_example"] = False

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


def instantiate_uri(URI_template, parameters):
    """Instantiate an URI template from a list of parameters

    Arguments:
    URI_template - URI template to be instanted
    parameters - List of URI parameters used for instantiating
    """
    # Find all the parameter blocks (ie. {var}, {?var1,var2}, etc). 

    processed_URI = ''
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
            #processed_URI += proccess_URI_parameter(URI_parameter)
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
                    processed_URI += prefix + parameters[i]['example']
                i += 1

            # If the parameter can not be found or it has not example value,
            # we replace it with "{prefix+var-name}" or simply ignore it 
            # depending on the type of parameter.
            if parameter_definition_found == False:
                if URI_parameter_block[0] != '?' and URI_parameter_block[0] != '&':
                    if URI_parameter_block[0] == '+':
                        prefix = '+'
                    URI_parameter_block_replace = URI_parameter_block_replace.replace(URI_parameter, "{" + prefix + URI_parameter + "}")
                    processed_URI += "{" + prefix + URI_parameter + "}"
                else:
                    URI_parameter_block_replace = URI_parameter_block_replace.replace(URI_parameter, '')
                    processed_URI += ''

        # Replace the original parameter block with the values of its members
        # omiting the separator character (',').
    
        URI_parameter_block_replace = URI_parameter_block_replace.replace(',','')
        URI_template = URI_template.replace("{" + URI_parameter_block + "}",processed_URI)

    return URI_template