{% macro render_metadata_toc(subsection) -%}
<li class="tocline"> <a href="#{{subsection.id}}" title = "{{subsection.name}}"> {{subsection.name}} </a>

    {% if subsection.subsections %}
        <ul class="toc">
        {% for subsubsection in subsection.subsections %}
            {{ render_metadata_toc(subsubsection) }}
        {% endfor %}
        </ul>
    {% endif%}
</li>

{%- endmacro %}
<div id="fiware-logo-container">
    <div id="fiware-logo"></div>
</div>
<nav id="toc">

        
    <ul class="toc">

        {% for metadata_value in metadata %}
	        {% if metadata_value.name == "TITLE" %}
		        <li><a href="#API-content">{{metadata_value.value}}</a></li>
	        {%endif%}
        {% endfor %}

{#Summary#}
<li><a href="#api-summary">API Summary</a></li>

{% for subsections in api_metadata.subsections %}
    {# {% for subsection in api_metadata.subsections[0].subsections %}#}
    {%if subsections.name != api_metadata.subsections[0].name %}
    <li>
        
        <a href="#{{subsections.id}}" title = "{{subsections.name}}" > {{subsections.name}} </a>
        
    <ul class="toc">
    {% for subsection in subsections.subsections %}
    {% if subsection.name in top_metadata %}
        {{ render_metadata_toc(subsection) }}
    {% endif %}
    {% endfor%}
   

{#  unespecified metadata #}
{% for subsection in subsections.subsections %}
    {% if not subsection.name in top_metadata  and not subsection.name in bottom_metadata and not subsection.name in intro_metadata %}
        {{ render_metadata_toc(subsection) }}
    {% endif %}
{% endfor%}

 </ul>
</li>
{% endif %}
{% endfor%}

{% if data_structures|length > 1 %}
    {# Common Payload Definition #}
    <li><a href="#common-payload-definition">Common Payload Definition</a></li>
{% endif %}



{# API #}
<li><a href="#API_specification">API Specification</a>
    <ul class="toc">
    {% for resourceGroup in resourceGroups %}

                        <li>
                            {% if resourceGroup.name|length > 1 %}
                                <a href="#{{ gen_resource_group_id( resourceGroup.name ) }}" title = "Group {{ resourceGroup.name }}">Group {{ resourceGroup.name }}</a>
                            {% else %}
                                <a href="#default_group" title = "Group default">Default</a>
                            {% endif %}
                            <ul class="toc">
                              {% for resource in resourceGroup.resources %}
                                {% if resource.ignoreTOC %}
                                    {% for action in resource.actions %}
                                        {% if action.name %}
                                            <li><a href="#{{ action.id }}" title = "{{action.method}} - {{ action.name }}">{{action.method}} - {{ action.name  }}</a></li>
                                        {% else %}
                                            {% if action.attributes.uriTemplate %}
                                                <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ action.attributes.uriTemplate }}">{{action.method}} - {{ action.attributes.uriTemplate }}  </a></li>
                                            {% else %}
                                                <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ resource.uriTemplate }}">{{action.method}} - {{ resource.uriTemplate }} </a></li>
                                            {% endif %}

                                        {% endif %}
                                        
                                    {% endfor %}
                                {% else %}
                                    <li>
                                        <a href="#{{ resource.id }}" title = "Resource {{ resource.name }}">Resource {{ resource.name }}</a>
                                        <ul class="toc  ">
                                        {% for action in resource.actions %}
                                            {% if action.name %}
                                                <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ action.name }}">{{action.method}} - {{ action.name }}</a></li>
                                            {% else %}
                                                {% if action.attributes.uriTemplate %}
                                                    <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ action.attributes.uriTemplate }}">{{action.method}} - {{ action.attributes.uriTemplate  }}</a></li>
                                                {% else %}
                                                    <li><a href="#{{ action.id }}" title ="{{action.method}}">{{action.method}}</a></li>
                                                {% endif %}
                                            {% endif %}

                                        {% endfor %}
                                        </ul>
                                    </li>
                                {% endif %}
                              {% endfor %}
                            </ul>
                        </li>
                      {% endfor %}
    <li><a href="#examples">Examples</a></li>
    </ul>
</li>
    {# bottom metadata #}
    {% for subsection in api_metadata.subsections[0].subsections %}
    {% if subsection.name in bottom_metadata %}
        {{ render_metadata_toc(subsection) }}
    {% endif %}
    {% endfor %}
    {%if reference_links|length > 0 %}
        <li><a href="#references">References</a></li>
    {% endif %}
   </ul>
</nav>

