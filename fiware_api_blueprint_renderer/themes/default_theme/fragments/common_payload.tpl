{% macro renderPayloadAttributes( attributes ) %}
    {% if attributes | length > 0 %}
        <dl>
            {% for attribute in attributes %}
                <dt>
                    {{ attribute.name }} 
                    {%- if attribute.required %}
                        (required,
                    {%- else %}
                        (optional,
                    {%- endif %}
                    {{ attribute.type }})
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
