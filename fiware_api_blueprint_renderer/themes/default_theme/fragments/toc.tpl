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
<section id="toc">
    <h2 id="h-toc" class="introductory">Table of contents</h2>
    <ul class="toc">

<!--medatada -->
       <!-- {{ render_metadata_toc(api_metadata.subsections[0]) }}-->

<!-- top metadata -->
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
   

<!-- unespecified metadata -->
{% for subsection in subsections.subsections %}
{#{% for subsection in api_metadata.subsections[0].subsections %}#}
    {% if not subsection.name in top_metadata  and not subsection.name in bottom_metadata and not subsection.name in intro_metadata %}
        {{ render_metadata_toc(subsection) }}
    {% endif %}
{% endfor%}

 </ul>
</li>
{% endif %}
{% endfor%}

<!-- Common Payload Definition -->
<li><a href="#common-payload-definition">Common Payload Definition</a></li>

<!-- API -->
<li><a href="#API_specification">API Specification</a>
    <ul class="toc">
    {% for resourceGroup in resourceGroups %}

                        <li>
                            <a href="#{{ gen_resource_group_id( resourceGroup.name ) }}" title = "Group {{ resourceGroup.name }}">Group {{ resourceGroup.name }}</a>
                            <ul class="toc">
                              {% for resource in resourceGroup.resources %}
                                {% if resource.ignoreTOC %}
                                    {% for action in resource.actions %}
                                        <li><a href="#{{ gen_action_id( action.name ) }}" title = "{{action.method}} - {{ action.name }}">{{action.method}} - {{ action.name }}</a></li>
                                    {% endfor %}
                                {% else %}
                                    <li>
                                        <a href="#{{ gen_resource_id( resource.name ) }}" title = "Resource {{ resource.name }}">Resource {{ resource.name }}</a>
                                        <ul class="toc  ">
                                        {% for action in resource.actions %}
                                            <li><a href="#{{ gen_action_id( action.name ) }}" title ="{{action.method}} - {{ action.name }}">{{action.method}} - {{ action.name }}</a></li>
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
    <!--bottom metadata -->
    {% for subsection in api_metadata.subsections[0].subsections %}
    {% if subsection.name in bottom_metadata %}
        {{ render_metadata_toc(subsection) }}
    {% endif %}
    {% endfor %}
    <li><a href="#references">References</a></li>
   </ul>
</section>

