{% macro displayActionHeader( id, action, resource ) %}
    <h4 id="{{id}}">
        {{ action.name }} -
        {{ action.method }}
        {% if action.attributes.uriTemplate | length > 0 %}
            {{ action.attributes.uriTemplate }}
        {% else %}
            {{ resource.uriTemplate }}
        {% endif %}
    </h4>
{% endmacro %}

{% macro gen_apiary_link( resourceGroupName, resourceName, resourceUri, actionName, actionMethod, metadata ) %}
    <div class="goApiary">
    {% for metadata_section in metadata %}
        {% if metadata_section['name'] == "APIARY_PROJECT" %}
            {% if resourceName | length > 0 %}
                {% set resource_slug = slug( resourceName ) %}
            {% else %}
                {% set resource_slug = slug( resourceUri ) |  replace( "/", "" ) | replace( "{", "" ) | replace( "}", "" ) | replace( ".", "" ) %}
            {% endif %}
            {% set resource_slug = resource_slug | replace( "*", "" ) %}

            {% if actionName | length > 0 %}
                {% set action_slug = slug( actionName ) %}
            {% else %}
                {% set action_slug = slug( actionMethod ) %}
            {% endif %}
            
                <a target="_blank" href="http://docs.{{ metadata_section['value'] }}.apiary.io/#reference/{{ slug( resourceGroupName ) }}/{{ resource_slug }}/{{ action_slug }}">View in Apiary</a>
            
        {% endif %}
    {% endfor %}
    </div>
{% endmacro %}

{% for resourceGroup in resourceGroups %}
        {% if resourceGroup.name|length > 0 %}
            <section id="{{ gen_resource_group_id( resourceGroup.name ) }}" class="resourceGroup">
            <h2 id="h-{{ gen_resource_group_id( resourceGroup.name ) }}">{{ resourceGroup.name }}</h2>
        {% else %}
            <section id="default_group" class="resourceGroup">
             <div class= "header" ><h2 id="h-default_group"> Default </h2></div>
        {% endif %}
	{{ resourceGroup.description }}
        {% for resource in resourceGroup.resources %}
            <section id="{{ resource.id }}" class="resource">
                 <div class= "header" ><h3 id="h-{{ gen_resource_id( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h3> </div>
                {{ resource.description }}
                {% set parameters = resource.parameters %}
                {% set parameters_definition_caption = "Parameters" %}

		        {# Display attributes #}
                {% set packet_contents = resource.content %}
                {% include "fragments/resource_attributes.tpl" %}

                {% include "fragments/parameters_definition.tpl" %}

                    {% for action in resource.actions %}
                        <div id="{{ action.id }}" class="action {{action.method}}">

                        {{ displayActionHeader( "h-" + gen_action_id( action.name ), action, resource ) }}
        
                            <div id="{{ slug( action.name ) }}_body" class="">
                                {{action.description}}
                                {% set parameters = action.parameters %}
                                {% set parameters_table_caption = "Parameters" %}
                                {% include "fragments/parameters_definition.tpl" %}			
                                {% set packet_contents = action.content %}
                                {% include "fragments/rest_packet_general_contents.tpl" %}      
                                    {% for example in action.examples %}
        	                            {% for request in example.requests %}
                                            {% set rest_packet = request %}
                                            {% set packet_type = "Request" %}
                                            {% set loop_index = loop.index %}
                                            {% include "fragments/rest_packet.tpl" %}
        	                            {% endfor %}
    
        	                            {% for response in example.responses %}
        		                            {% set rest_packet = response %}
                                        {% set packet_type = "Response" %}
                                        {% set loop_index = loop.index %}
                                        {% include "fragments/rest_packet.tpl" %}
        	                            {% endfor %}
                                    {% endfor %}
                                    
                                    <div class="goExample">
                                        <a href="#{{ action.id }}_examples">Go to example</a>
                                    </div>
                                    {% if resourceGroup.name|length > 0 %}
                                        {{ gen_apiary_link( resourceGroup.name, resource.name, resource.uriTemplate, action.name, action.method, metadata ) }}
                                    {% else %}
                                        {{ gen_apiary_link( "Default", resource.name, resource.uriTemplate, action.name, action.method, metadata ) }}
                                    {% endif %}
                                
                            </div>
                        </div>
                    {% endfor %}
            </section>
        {% endfor %}
    </section>
{% endfor %}
<section id="examples">
    <div class= "header" ><h2>Examples</h2> </div>
    {% for resourceGroup in resourceGroups %}
        {% if resourceGroup.name|length > 0 %}
            <section id="{{ gen_resource_group_example_id( resourceGroup.name ) }}" class="resourceGroupExample">
                <div class= "header" ><h3 id="h-{{ gen_resource_group_example_id( resourceGroup.name ) }}">{{ resourceGroup.name }}</h3> </div>
        {% else %}
            <section id="{{ gen_resource_group_example_id( resourceGroup.name ) }}" class="resourceGroupExample">
                <div class= "header" ><h3 id="h-{{ gen_resource_group_example_id( resourceGroup.name ) }}">Default</h3> </div>
        {% endif %}

                {% for resource in resourceGroup.resources %}
                    <section id="{{ gen_resource_example_id( resource.name ) }}" class="resourceExample">
                         <div class= "header" ><h4 id="h-{{ gen_resource_example_id( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h4></div>
                            
                            {% set parameters = resource.parameters %}
                            {% set parameters_definition_caption = "Parameters" %}

                            {#  Display attributes #}
                            {% set packet_contents = resource.content %}
                            {# {% include "fragments/resource_attributes.tpl" %} #}

                            {% include "fragments/parameters_definition.tpl" %}

                            {% for action in resource.actions %}
                                <div id="{{ action.id }}_examples" class="actionExample {{action.method}}">

                                    {{ displayActionHeader( "h-" + gen_action_id( action.name ) + "_examples", action, resource ) }}
                
                                    <div id="{{ gen_action_id( action.name ) }}_body" class=""> 
                                        {% set parameters = action.parameters %}
                                        {% set parameters_table_caption = "Parameters" %}
                                        
                                        {% include "fragments/parameters_definition.tpl" %}         
                                        {% set packet_contents = action.content %}
                                        {#{% include "fragments/rest_packet_general_contents.tpl" %}  #}    
                                            {% for example in action.examples %}
                                                {% for request in example.requests %}
                                                    {% set rest_packet = request %}
                                                    {% set packet_type = "Request" %}
                                                    {% set loop_index = loop.index %}
                                                    {% include "fragments/rest_packet_examples.tpl" %}
                                                {% endfor %}
            
                                                {% for response in example.responses %}
                                                    {% set rest_packet = response %}
                                                {% set packet_type = "Response" %}
                                                {% set loop_index = loop.index %}
                                                {% include "fragments/rest_packet_examples.tpl" %}
                                                {% endfor %}
                                            {% endfor %}
                                            <div class="goActions">
                                                <a href="#{{ action.id }}">Go to specification</a>
                                            </div>
                                    </div>
                                </div>
                            {% endfor %}
                    </section>
            {% endfor %}
        </section>
    {% endfor %}



</section>
