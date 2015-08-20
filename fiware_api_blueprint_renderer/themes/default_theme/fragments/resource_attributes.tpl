{%- macro displayTypeName( nameObject ) %}
    {%- if nameObject.literal is defined %}{{ nameObject.literal }}
    {%- else %}{{ nameObject }}
    {%- endif %}
{%- endmacro %}

{% macro displayPacketProperties( packetContent ) %}
    <dl class="action-parameters-table">
        {%- for section_content in packetContent %}
            {%- if section_content.class == "property" %}
                    <dt>{{ section_content.content.name.literal }}
                    (
                    {%-if("required" in section_content.content.valueDefinition.typeDefinition.attributes) -%}
                        Required
                    {%- else -%}
                        Not required
                    {%- endif -%}
                    ,
                    {{ displayTypeName( section_content.content.valueDefinition.typeDefinition.typeSpecification.name ) }}
                    {%- if section_content.content.valueDefinition.typeDefinition.typeSpecification.name == "array" %}
                        [{{ section_content.content.valueDefinition.typeDefinition.typeSpecification.nestedTypes[0] }}]
                    {%- endif %})
                    </dt>
                    <dd>
                        {{ section_content.content.description }}
                        {% if displayTypeName( section_content.content.valueDefinition.typeDefinition.typeSpecification.name ) == "object" and
                            section_content.content.sections | length > 0 %}
                            {{ displayPacketProperties( section_content.content.sections[0].content ) }}
                        {% endif %}
                    </dd>
            {%- endif %}
        {%- endfor %}
    </dl> 
{% endmacro %}

{% macro displayPacketContents( packetContents ) %}
    {% if packetContents | length > 0 and packetContents[0]["typeDefinition"] is defined %}
        <span class="payload-title">Payload</span>
        {% for content in packetContents %}
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
                            {{ displayPacketProperties( section.content ) }}
                        {%- endif %}
                    {%- endfor %}
                {%- endif %}
            {% endif %}
        {% endfor %}
    {% endif %}
{% endmacro %}

{{ displayPacketContents( packet_contents ) }}
