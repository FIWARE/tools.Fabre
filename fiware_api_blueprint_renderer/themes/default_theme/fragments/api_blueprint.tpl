{% for resourceGroup in resourceGroups %}
        <section id="{{ slug( resourceGroup.name ) }}" class="resourceGroup">
        <h2 id="h-{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</h2>
        {% for resource in resourceGroup.resources %}
            <section id="{{ slug( resource.name ) }}" class="resource">
                <h3 id="h-{{ slug( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h3>
                {{ resource.description }}
                {% set parameters = resource.parameters %}
                {% set parameters_definition_caption = "Parameters" %}

		        <!-- Display attributes -->
                {% set packet_contents = resource.content %}
                {% include "fragments/resource_attributes.tpl" %}

                {% include "fragments/parameters_definition.tpl" %}
                <h4>Actions</h4>
                    {% for action in resource.actions %}
                        <div id="{{ slug( action.name ) }}" class="action {{action.method}}">
                        <h5 id="h-{{ slug( action.name ) }}"> {{ action.name }}</h5>
                            <div class="action-header">
                                    <span class="action-method">{{ action.method }} </span>
                                    <span class="action-uri">
                                      {% if action.attributes.uriTemplate | length > 0 %}
                                        {{ action.attributes.uriTemplate }}
                                    {% else %}
                                        {{ resource.uriTemplate }}
                                    {% endif %}
                                    </span>
                                
                                    <!--<em class="action-name"> action nameeeee {{ action.name }}</em>-->
                            </div>  
        
                            <div id="{{ slug( action.name ) }}_body" class=""> 
                                <p>{{ action.description }}</p>
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
                                        <a href="#{{ slug( action.name ) }}_examples">Go to example</a>
                                    </div>
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
        <section id="{{ slug( resourceGroup.name ) }}_example" class="resourceGroupExample">
            <h3 id="h-{{ slug( resourceGroup.name ) }}_example">{{ resourceGroup.name }}</h3>
            {% for resource in resourceGroup.resources %}
                <section id="{{ slug( resource.name ) }}_example" class="resourceExample">
                    <h4 id="h-{{ slug( resource.name ) }}_example">{{ resource.name }} [{{ resource.uriTemplate}}]</h4>
                        {% for action in resource.actions %}
                            <div id="{{ slug( action.name ) }}_examples" class="actionExample {{action.method}}">
                            <h5 id="h-{{ slug( action.name ) }}_examples"> {{ action.name }} </h5>
                                <div class="action-header">
                                        <span class="action-method">{{ action.method }} </span>
                                        <span class="action-uri">
                                          {% if action.attributes.uriTemplate | length > 0 %}
                                            {{ action.attributes.uriTemplate }}
                                        {% else %}
                                            {{ resource.uriTemplate }}
                                        {% endif %}
                                        </span>
                                    
                                        <!--<em class="action-name"> action nameeeee {{ action.name }}</em>-->
                                </div>  
            
                                <div id="{{ slug( action.name ) }}_body" class=""> 
                                   {# <p>{{ action.description }}</p> #}
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
                                            <a href="#{{ slug( action.name ) }}">Go to specification</a>
                                        </div>
                                </div>
                            </div>
                        {% endfor %}
                </section>
            {% endfor %}
        </section>
    {% endfor %}



</section>
