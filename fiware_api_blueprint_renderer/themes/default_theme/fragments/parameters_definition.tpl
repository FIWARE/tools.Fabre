<!-- Action parameters -->     
{% if parameters|length > 0 %}
	<span class="parameters-title">Parameters</span>
	<dl>
		{% for parameter in parameters %}
			<dt>
				{{ parameter.name }} (
				{%- if parameter.required -%}
					Required
				{%- else -%}
					Optional
				{%- endif -%}
				, {{ parameter.type }} )
			</dt>
			<dd>
				{{ parameter.description }}
			</dd>
		{% endfor %}
	</dl>
{% endif %}
