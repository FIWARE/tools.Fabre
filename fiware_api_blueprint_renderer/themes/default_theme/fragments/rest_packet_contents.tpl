{%- macro displayTypeName( nameObject ) %}
    {%- if nameObject.literal is defined %}{{ nameObject.literal }}
    {%- else %}{{ nameObject }}
    {%- endif %}
{%- endmacro %}
{% if packet_contents | length > 0 and packet_contents[0]["typeDefinition"] is defined %}
    <span class="payload-title">Payload</span>
    {% for content in packet_contents %}
        {% if content["typeDefinition"] %}
            {%- if content["typeDefinition"] is defined and displayTypeName( content["typeDefinition"]["typeSpecification"]["name"] ) != "object" and data_structures[ displayTypeName(content["typeDefinition"]["typeSpecification"]["name"])] %}
                {% from 'fragments/common_payload.tpl' import renderPayloadAttributes %}
                {% set attributes = data_structures[ displayTypeName(content["typeDefinition"]["typeSpecification"]["name"])]["attributes"] %}
                {{ renderPayloadAttributes( attributes ) }}
                {#{% include "fragments/parameters_definition.tpl" %}#}
            {% endif %}
            {%- if content["sections"] is defined %}
                {%- for section in content["sections"] %}
                    {%- if section.class == "memberType" %}
                        <dl class="action-parameters-table">

                        {%- for section_content in section.content | sort_payload_parameters %}
                            {%- if section_content.class == "property" %}
                                    <dt><span class="parameter-name">{{ section_content.content.name.literal }}</span>
                                    <span class="parameter-attributes">(
                                    {%-if("required" in section_content.content.valueDefinition.typeDefinition.attributes) -%}
                                        Required
                                    {%- else -%}
                                        Not required
                                    {%- endif -%}
                                    ,
                                    {{ displayTypeName( section_content.content.valueDefinition.typeDefinition.typeSpecification.name ) }}
                                    {%- if section_content.content.valueDefinition.typeDefinition.typeSpecification.name == "array" %}
                                        [{{ section_content.content.valueDefinition.typeDefinition.typeSpecification.nestedTypes[0] }}]
                                    {%- endif %})</span>
                                    </dt>
                                    <dd>{{ section_content.content.description }}</dd>
                            {%- endif %}
                        {%- endfor %}
                        </dl> 
                      
                    {%- endif %}
                {%- endfor %}
            {%- endif %}
        {% endif %}
    {% endfor %}
{% endif %}
