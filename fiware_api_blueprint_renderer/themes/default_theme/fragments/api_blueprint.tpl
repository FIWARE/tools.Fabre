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

{% macro gen_apiary_link( resourceGroupName, resourceName, actionName, metadata ) %}
    {% for metadata_section in metadata %}
        {% if metadata_section['name'] == "APIARY_PROJECT" %}
            <div class="goApiary">
                <a target="_blank" href="http://docs.{{ metadata_section['value'] }}.apiary.io/#reference/{{ slug( resourceGroupName ) }}/{{ slug( resourceName ) }}/{{ slug( actionName ) }}">View in Apiary</a>
            </div>
        {% endif %}
    {% endfor %}
{% endmacro %}

{% for resourceGroup in resourceGroups %}
        <section id="{{ gen_resource_group_id( resourceGroup.name ) }}" class="resourceGroup">
        <h2 id="h-{{ gen_resource_group_id( resourceGroup.name ) }}">{{ resourceGroup.name }}</h2>
	{{ resourceGroup.description }}
        {% for resource in resourceGroup.resources %}
            <section id="{{ gen_resource_id( resource.name ) }}" class="resource">
                <h3 id="h-{{ gen_resource_id( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h3>
                {{ resource.description }}
                {% set parameters = resource.parameters %}
                {% set parameters_definition_caption = "Parameters" %}

		        {# Display attributes #}
                {% set packet_contents = resource.content %}
                {% include "fragments/resource_attributes.tpl" %}

                {% include "fragments/parameters_definition.tpl" %}

                    {% for action in resource.actions %}
                        <div id="{{ gen_action_id( action.name ) }}" class="action {{action.method}}">

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
                                        <a href="#{{ gen_action_id( action.name ) }}_examples">Go to example</a>
                                    </div>

                                    {{ gen_apiary_link( resourceGroup.name, resource.name, action.name, metadata ) }}
                            </div>
                        </div>
                    {% endfor %}
            </section>
        {% endfor %}
    </section>
{% endfor %}
<section id="examples">
    <h2>Examples</h2>
    {% for resourceGroup in resourceGroups %}
        <section id="{{ gen_resource_group_example_id( resourceGroup.name ) }}" class="resourceGroupExample">
            <h3 id="h-{{ gen_resource_group_example_id( resourceGroup.name ) }}">{{ resourceGroup.name }}</h3>

            {% for resource in resourceGroup.resources %}
                <section id="{{ gen_resource_example_id( resource.name ) }}" class="resourceExample">
                    <h4 id="h-{{ gen_resource_example_id( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h4>
                        
                        {% set parameters = resource.parameters %}
                        {% set parameters_definition_caption = "Parameters" %}

                        {#  Display attributes #}
                        {% set packet_contents = resource.content %}
                        {# {% include "fragments/resource_attributes.tpl" %} #}

                        {% include "fragments/parameters_definition.tpl" %}

                        {% for action in resource.actions %}
                            <div id="{{ gen_action_id( action.name ) }}_examples" class="actionExample {{action.method}}">

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
                                            <a href="#{{ gen_action_id( action.name ) }}">Go to specification</a>
                                        </div>
                                </div>
                            </div>
                        {% endfor %}
                </section>
            {% endfor %}
        </section>
    {% endfor %}



</section>
