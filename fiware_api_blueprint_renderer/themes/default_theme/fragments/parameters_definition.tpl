{# Action parameters #}
{% if parameters|length > 0 %}
	<span class="parameters-title">Parameters</span>
	<dl>
		{% for parameter in parameters | sort(attribute='name') %}
			<dt>
				<span class="parameter-name">{{ parameter.name }}</span> <span class="parameter-attributes">(
				{%- if parameter.required -%}
					Required
				{%- else -%}
					Optional
				{%- endif -%}
				{%- if parameter.type -%}
					, {{ parameter.type }}
				{%- endif -%})</span>
			</dt>
			<dd>
				{{ parameter.description }}
				{% if parameter["values"] %}
					<p>Allowed values:</p>
					<dl>
						{% for value in parameter["values"] %}
							<dt>
								{{ value.value }} 
							</dt>
							<dd>
								{{ value.description }}
							</dd>
						{% endfor %}
					</dl>
				{% endif %}
			</dd>
		{% endfor %}
	</dl>
{% endif %}
