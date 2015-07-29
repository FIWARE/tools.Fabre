{%- macro displayTypeName( nameObject ) %}
    {%- if nameObject.literal is defined %}{{ nameObject.literal }}
    {%- else %}{{ nameObject }}
    {%- endif %}
{%- endmacro %}

{% if packet_contents | length > 0 and packet_contents[0]["typeDefinition"] is defined %}
    <p>Payload</p>
    {% for content in packet_contents %}
        {% if content["typeDefinition"] %}
            {%- if content["typeDefinition"] is defined and displayTypeName( content["typeDefinition"]["typeSpecification"]["name"] ) != "object" and data_structures[ displayTypeName(content["typeDefinition"]["typeSpecification"]["name"])] %}
                <table class="action-parameters-table">
                    <tr>
                        <th class="action-parameters-th">Name</th>
                        <th class="action-parameters-th">Required</th>
                        <th class="action-parameters-th">Type</th>
                        <th class="action-parameters-th">Description</th>
                    </tr>

                {%- for attribute in data_structures[ displayTypeName(content["typeDefinition"]["typeSpecification"]["name"])]["attributes"] %}
                    <tr>
                        <td class="action-parameters-td">{{ attribute["name"] }}</td>
                        <td class="action-parameters-th">{{ attribute["required"] }}</td>
                        <td class="action-parameters-td">{{ attribute["type"] }}</td>
                        <td class="action-parameters-td">{{ attribute['description'] }}</td>
                    </tr>
                {%- endfor %}
                </table>
            {% endif %}
            {%- if content["sections"] is defined %}
                {%- for section in content["sections"] %}
                    {%- if section.class == "memberType" %}
    			        <div class="col-md-12 no-padding">
                            <table class="action-parameters-table">
                                <tr>
                                    <th class="action-parameters-th">Name</th>
                                    <th class="action-parameters-th">Required</th>
                                    <th class="action-parameters-th">Type</th>
                                    <th class="action-parameters-th">Description</th>
                                </tr>
                            {%- for section_content in section.content %}
                                {%- if section_content.class == "property" %}
                                    <tr>
                                        <td class="action-parameters-td">{{ section_content.content.name.literal }}</td>
                                        <td class="action-parameters-th">
                                        {% print("required" in section_content.content.valueDefinition.typeDefinition.attributes) %}
                                        </td>
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
                        </div>
                    {%- endif %}
                {%- endfor %}
            {%- endif %}
        {% endif %}
    {% endfor %}
{% endif %}
