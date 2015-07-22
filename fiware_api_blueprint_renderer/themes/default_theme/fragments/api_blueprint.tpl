{% for resourceGroup in resourceGroups %}
    <h2 id="{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</h2>
    {% for resource in resourceGroup.resources %}
        <h3 id="{{ slug( resource.name ) }}">{{ resource.name }} [{{ resource.uriTemplate}}]</h3>
        {{ resource.description }}
        {% set parameters = resource.parameters %}
        {% include "fragments/parameters_table.tpl" %}
        <h4>Actions</h4>
            {% for action in resource.actions %}
                <div id="{{ slug( action.name ) }}" class="action-div">
                    <div class="row action-div-header">
                        <div class="col-md-1">
                            <div class="action-method">{{ action.method }}</div>
                        </div>
                        <div class="col-md-5">
                            <div class="action-uri">
                            {% if action.attributes.uriTemplate | length > 0 %}
                                {{ action.attributes.uriTemplate }}
                            {% else %}
                                {{ resource.uriTemplate }}
                            {% endif %}
                            </div>
                        </div>
                        <div class="col-md-4">
                            <em class="action-name">{{ action.name }}</em>
                        </div>
                        <div class="col-md-2 toogle-button">
                            <a href="#{{ slug( action.name ) }}_body" class="btn btn-default" data-toggle="collapse">detail</a>
                        </div>
                    </div>

                    <div id="{{ slug( action.name ) }}_body" class="collapse action-div-body">
                        <p>{{ action.description }}</p>
                        {% set parameters = action.parameters %}
                        {% include "fragments/parameters_table.tpl" %}			
                        {% set packet_contents = action.content %}
                        {% include "fragments/rest_packet_contents.tpl" %}      
                            {% for example in action.examples %}
	                            {% for request in example.requests %}
                                {% set rest_packet = request %}
                                {% set packet_type = "request" %}
                                {% set loop_index = loop.index %}
                                {% include "fragments/rest_packet.tpl" %}
	                            {% endfor %}

	                            {% for response in example.responses %}
		                            {% set rest_packet = response %}
                                {% set packet_type = "response" %}
                                {% set loop_index = loop.index %}
                                {% include "fragments/rest_packet.tpl" %}
	                            {% endfor %}
                            {% endfor %}
                    </div>
                </div>
            {% endfor %}
    {% endfor %}
{% endfor %}
