{% macro renderPayloadAttributes( attributes ) %}
    {% if attributes | length > 0 %}
        <dl>
            {% for attribute in attributes | sort(attribute='name') %}
                <dt>
                    <span class="parameter-name">{{ attribute.name }}</span>
                    {%- if attribute.required %}
                        <span class="parameter-attributes">(required,
                    {%- else %}
                        <span class="parameter-attributes">(optional,
                    {%- endif %}
                    {{ attribute.type }})</span>
                </dt>
                <dd>
                    {{ attribute.description }}
                    {% if attribute.subproperties | length > 0 %}
                        {{ renderPayloadAttributes( attribute.subproperties ) }}
                    {% endif %}
                </dd>
            {% endfor %}
        </dl>
    {% endif %}
{% endmacro %}
