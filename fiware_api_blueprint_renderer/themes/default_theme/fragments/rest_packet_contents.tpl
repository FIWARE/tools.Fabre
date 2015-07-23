{%- macro displayTypeName( nameObject ) %}
    {%- if nameObject.literal is defined %}{{ nameObject.literal }}
    {%- else %}{{ nameObject }}
    {%- endif %}
{%- endmacro %}

{% if packet_contents | length > 0 and packet_contents[0]["typeDefinition"] is defined %}
    <p>Body attributes</p>
    {% for content in packet_contents %}
        {% if content["typeDefinition"] %}
            {%- if content["typeDefinition"] is defined and displayTypeName( content["typeDefinition"]["typeSpecification"]["name"] ) != "object" %}
                {{ displayTypeName( content["typeDefinition"]["typeSpecification"]["name"] ) }}{% endif %}
            {%- if content["sections"] is defined %}
                {%- for section in content["sections"] %}
                    {%- if section.class == "memberType" %}
			            <table class="action-parameters-table">
                            <tr>
                                <th class="action-parameters-th">Name</th>
                                <th class="action-parameters-th">Type</th>
                                <th class="action-parameters-th">Description</th>
                            </tr>
                        {%- for section_content in section.content %}
                            {%- if section_content.class == "property" %}
                                <tr>
                                    <td class="action-parameters-td">{{ section_content.content.name.literal }}</td>
                                    <td class="action-parameters-td">{{ displayTypeName( section_content.content.valueDefinition.typeDefinition.typeSpecification.name ) }}
                                    {% if section_content.content.valueDefinition.typeDefinition.typeSpecification.name == "array" %}
                                        [{{ section_content.content.valueDefinition.typeDefinition.typeSpecification.nestedTypes[0] }}]
                                    {% endif %}
                                    </td>
                                    <td class="action-parameters-td">{{ section_content.content.description }}</td>
                                </tr>
                            {%- endif %}
                        {%- endfor %}
                        </table>
                    {%- endif %}
                {%- endfor %}
            {%- endif %}
        {% endif %}
    {% endfor %}
{% endif %}
