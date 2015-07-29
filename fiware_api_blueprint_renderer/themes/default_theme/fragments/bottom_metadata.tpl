
{% macro render_subsection(subsection, level) -%}
<h{{ level }} id="{{ subsection.id }}"> {{subsection.name}}</h{{ level }}>
{{subsection.body}}

{% for subsubsection in subsection.subsections %}
{{ render_subsection(subsubsection, level+1) }}
{% endfor %}

{%- endmacro %}

{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name in bottom_metadata %}
	  	<section>
			{{ render_subsection(subsection,1) }}
		</section>
	{% endif %}
{% endfor%}