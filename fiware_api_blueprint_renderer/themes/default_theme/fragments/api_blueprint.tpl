{% macro displayActionHeader( id, action, resource, header_level ) %}
    <div class="header">
        {% if action.name %}
            <h{{header_level}} id="{{id}}">{{ action.name }} </h{{header_level}}>
            <span class="extra-header">
		{{ action.method }} 
                {% if action.attributes.uriTemplate | length > 0 %}
                    {{ action.attributes.uriTemplate }}
                {% else %}
                    {{ resource.uriTemplate }}
                {% endif %}
            </span>
        {% else %}
            <h{{header_level}} id="{{id}}"> {{ action.method }} - 
            {% if action.attributes.uriTemplate | length > 0 %}
                {{ action.attributes.uriTemplate }}
            {% else %}
                {{ resource.uriTemplate }}
            {% endif %}
            </h{{header_level}}>

        {% endif %}

    </div>
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
                 <div class= "header" >
                 {% if resource.name %}
                    <h3 id="h-{{ gen_resource_id( resource.name ) }}">{{ resource.name }}</h3>
                    <span class="extra-header">[{{ resource.uriTemplate}}]</span>
                 {% else %}
                    <h3 id="h-{{ gen_resource_id( resource.name ) }}">[{{ resource.uriTemplate}}]</h3>
                 {% endif %}
                 </div>
                {{ resource.description }}
                {% set parameters = resource.parameters %}
                {% set parameters_definition_caption = "Parameters" %}

		        {# Display attributes #}
                {% set packet_contents = resource.content %}
                {% include "fragments/resource_attributes.tpl" %}

                {% include "fragments/parameters_definition.tpl" %}

                    {% for action in resource.actions %}
                        <div id="{{ action.id }}" class="action {{action.method}}">

                        {{ displayActionHeader( "h-" + gen_action_id( action.name ), action, resource, '4'  ) }}
        
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

                                        {%- if rest_packet.is_example == False -%}
                                            {% set first_found = True %}
                                            {% include "fragments/rest_packet.tpl" %}

                                            {# Display resposnes if they exist #}
                                            {%- if example.responses|length != 0 -%}

                                                {# If there are less responses than requests, 
                                                use the last defined response #}
                                                {%- if loop.index < example.responses|length -%}
                                                    {% set response_index = loop_index %}
                                                {%- else -%}
                                                    {% set response_index = example.reponses|length %}
                                                {%- endif -%}

                                                {% set rest_packet = example.responses[response_index] %}
                                                {% set packet_type = "Response" %}
                                                {% set loop_index = loop.index %}
                                                {% include "fragments/rest_packet.tpl" %}

                                            {%- endif -%}

                                        {%- endif -%}
    	                            {% endfor %}
                                {% endfor %}
                                <div>
                                {%- if action["has_example"] -%}
                                    <div class="goExample">
                                        <a href="#{{ action.id }}_examples">Go to example</a>
                                    </div>
                                {%- endif -%}
                                {% if resourceGroup.name|length > 0 %}
                                    {{ gen_apiary_link( resourceGroup.name, resource.name, resource.uriTemplate, action.name, action.method, metadata ) }}
                                {% else %}
                                    {{ gen_apiary_link( "Default", resource.name, resource.uriTemplate, action.name, action.method, metadata ) }}
                                {% endif %}
                                </div>
                                
                            </div>
                        </div>
                    {% endfor %}
            </section>
        {% endfor %}
    </section>
{% endfor %}

{# Display Example section if at least one group has one example #}
{%- if has_example -%}

<section id="examples">
    <div class= "header" ><h2>Examples</h2> </div>
    {% for resourceGroup in resourceGroups %}

        {# Display Group if it has at least one example #}
        {%- if resourceGroup["has_example"] -%}
            {% if resourceGroup.name|length > 0 %}
                {% set resource_group_name = resourceGroup.name %}
            {% else %}
                {% set resource_group_name = "Default" %}
            {% endif %}

            <section id="{{ gen_resource_group_example_id( resourceGroup.name ) }}" class="resourceGroupExample">
                <div class= "header" ><h3 id="h-{{ gen_resource_group_example_id( resourceGroup.name ) }}">{{resource_group_name}}</h3> </div>
                
                {% for resource in resourceGroup.resources %}
                    {# Display Resource if it has at least one example #}
                    {%- if resource["has_example"] -%}
                        <section id="{{ gen_resource_example_id( resource.name ) }}" class="resourceExample">
                            <div class= "header" >
                            {%if resource.name %}
                                <h4 id="h-{{ gen_resource_example_id( resource.name ) }}">{{ resource.name }}</h4>
                                <span class="extra-header">[{{ resource.uriTemplate}}]</span>
                            {% else %}
                                <h4 id="h-{{ gen_resource_example_id( resource.name ) }}">[{{ resource.uriTemplate}}]</h4>
                            {% endif %}
                            </div>

                            {% set parameters = resource.parameters %}
                            {% set parameters_definition_caption = "Parameters" %}

                            {#  Display attributes #}
                            {% set packet_contents = resource.content %}
                            {# {% include "fragments/resource_attributes.tpl" %} #}

                            {# {% include "fragments/parameters_definition.tpl" %} #}

                            {% for action in resource.actions %}
                                {# Display Action if it has at least one example #}
                                {%- if action["has_example"] -%}
                                    <div id="{{ action.id }}_examples" class="actionExample {{action.method}}">

                                    {{ displayActionHeader( "h-" + gen_action_id( action.name ) + "_examples", action, resource, '5' ) }}
                                
                                        <div id="{{ gen_action_id( action.name ) }}_body" class=""> 
                                            {% set parameters = action.parameters %}
                                            {% set parameters_table_caption = "Parameters" %}
                                            
                                            {#{% include "fragments/parameters_definition.tpl" %} #}         
                                            {% set packet_contents = action.content %}
                                            {#{% include "fragments/rest_packet_general_contents.tpl" %}  #}    
                                            {% for example in action.examples %}

                                                {% for request in example.requests %}
                                                    {% set rest_packet = request %}
                                                    {% set packet_type = "Request" %}
                                                    {% set loop_index = loop.index %}

                                                    {% if rest_packet.is_example == True %}
                                                        {% include "fragments/rest_packet_examples.tpl" %}

                                                        {# Display resposnes if they exist #}
                                                        {%- if example.responses|length != 0 -%}

                                                            {# If there are less responses than requests, 
                                                            use the last defined response #}
                                                            {%- if loop.index < example.responses|length -%}
                                                                {% set response_index = loop_index %}
                                                            {%- else -%}
                                                                {% set response_index = example.reponses|length %}
                                                            {%- endif -%}

                                                            {% set rest_packet = example.responses[response_index] %}
                                                            {% set packet_type = "Response" %}
                                                            {% set loop_index = loop.index %}
                                                            {% include "fragments/rest_packet_examples.tpl" %}

                                                        {%- endif -%}
                                                    {% endif %}
                                                {% endfor %}
                                            {% endfor %}
                                            <div class="goActions">
                                                <a href="#{{ action.id }}">Go to specification</a>
                                            </div>
                                        </div>
                                    </div>
                                {%- endif -%}
                            {% endfor %}
                        </section>
                    {% endif %}
                {% endfor %}
            </section>
        {% endif %}
    {% endfor %}
</section>
{% endif %}
