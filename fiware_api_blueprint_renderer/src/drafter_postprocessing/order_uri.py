
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
