{% macro render_metadata_toc(subsection) -%}
<li class="tocline"> <a href="#{{subsection.id}}" > {{subsection.name}} </a>

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
        
        <a href="#{{subsections.id}}" > {{subsections.name}} </a>
        
    <ul class="toc">
    {% for subsection in subsections.subsections %}
    {% if subsection.name in top_metadata %}
        <section>
            {{ render_metadata_toc(subsection) }}
        </section>
    {% endif %}
    {% endfor%}
   

<!-- unespecified metadata -->
{% for subsection in subsections.subsections %}
{#{% for subsection in api_metadata.subsections[0].subsections %}#}
    {% if not subsection.name in top_metadata  and not subsection.name in bottom_metadata and not subsection.name in intro_metadata %}
        <section>
            {{ render_metadata_toc(subsection) }}
        </section>
    {% endif %}
{% endfor%}

 </ul>
</li>
{% endif %}
{% endfor%}
<!-- API -->
<li><a href="#API_specification">API Specification</a>
    <ul class="toc">
    {% for resourceGroup in resourceGroups %}

                        <li>
                            <a href="#{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</a>
                            <ul class="toc">
                              {% for resource in resourceGroup.resources %}
                                {% if resource.ignoreTOC %}
                                    {% for action in resource.actions %}
                                        <li><a href="#{{ slug( action.name ) }}">{{ action.name }}</a></li>
                                    {% endfor %}
                                {% else %}
                                    <li>
                                        <a href="#{{ slug( resource.name ) }}">{{ resource.name }}</a>
                                        <ul>
                                        {% for action in resource.actions %}
                                            <li><a href="#{{ slug( action.name ) }}">{{ action.name }}</a></li>
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
        <section>
            {{ render_metadata_toc(subsection) }}
        </section>
    {% endif %}
    {% endfor %}
    <li><a href="#references">References</a></li>
   </ul>
</section>

