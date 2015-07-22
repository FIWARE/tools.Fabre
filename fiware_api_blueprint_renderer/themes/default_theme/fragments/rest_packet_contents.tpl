{%- macro displayTypeName( nameObject ) %}
    {%- if nameObject.literal is defined %}"type": "{{ nameObject.literal }}",
    {%- else %}"type": "{{ nameObject }}",
    {%- endif %}
{%- endmacro %}

{% if packet_contents | length > 0 and packet_contents[0]["typeDefinition"] is defined %}
    <p>Content</p>
    {% for content in packet_contents %}
        {% if content["typeDefinition"] %}
            <pre><code>{
            {%- if content["typeDefinition"] is defined %}
                {{ displayTypeName( content["typeDefinition"]["typeSpecification"]["name"] ) }}{% endif %}
            {%- if content["sections"] is defined %}
                {%- for section in content["sections"] %}
                    {%- if section.class == "memberType" %}
                        "properties": {
                        {%- for section_content in section.content %}
                            {%- if section_content.class == "property" %}
                                "{{ section_content.content.name.literal }}": {
                                    {{ displayTypeName( section_content.content.valueDefinition.typeDefinition.typeSpecification.name ) }}
                                    "description": "{{ section_content.content.description }}",
                                    },
                            {%- endif %}
                        {%- endfor %}
                        },
                    {%- endif %}
                {%- endfor %}
            {%- endif %}
            }</code></pre>
        {% endif %}
    {% endfor %}
{% endif %}
