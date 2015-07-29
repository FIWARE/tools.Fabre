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
    <h2 id="h-toc" class="introductory"></h2>
    <ul>

<!--medatada -->
        {{ render_metadata_toc(api_metadata.subsections[0]) }}

<!-- API -->
    {% for resourceGroup in resourceGroups %}
                        <li>
                            <a href="#{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</a>
                            <ul>
                              {% for resource in resourceGroup.resources %}
                                <li>
                                    <a href="#{{ slug( resource.name ) }}">{{ resource.name }}</a>
                                    <ul>
                                    {% for action in resource.actions %}
                                        <li><a href="#{{ slug( action.name ) }}">{{ action.name }}</a></li>
                                    {% endfor %}
                                    </ul>
                                </li>
                              {% endfor %}
                            </ul>
                        </li>
                      {% endfor %}

   </ul>
</section>

