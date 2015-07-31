
{% macro render_subsection(subsection, level) -%}
<h{{ level }} id="{{ subsection.id }}"> {{subsection.name}}</h{{ level }}>
{{subsection.body}}

{% for subsubsection in subsection.subsections %}
{{ render_subsection(subsubsection, level+1) }}
{% endfor %}

{%- endmacro %}

<section>
<!-- specified top metadata -->
{% for subsections in api_metadata.subsections %}
	{# {% for subsection in api_metadata.subsections[0].subsections %} #}
	<section>
		{%if subsections.name != api_metadata.subsections[0].name %}
			<h1 id="{{subsections.id}}">{{subsections.name}}</h1>
		{% endif %}
	</section>
	{% for subsection in subsections.subsections %}
		{% if subsection.name in top_metadata %}
		  	<section>
				{{ render_subsection(subsection,2) }}
			</section>
		{% endif %}
	{% endfor%}


<!-- unespecified metadata -->

	{# {% for subsection in api_metadata.subsections[0].subsections %} #}
	{% for subsection in subsections.subsections[1:] %}
		{% if subsection.name not in top_metadata  and  subsection.name not in bottom_metadata and  subsection.name not in intro_metadata %}
			<section>
				{{ render_subsection(subsection,2) }}
			</section>
		{% endif %}
	{% endfor%}

{% endfor %}

</section>