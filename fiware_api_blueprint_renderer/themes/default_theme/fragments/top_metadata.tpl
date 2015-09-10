
{% macro render_subsection(subsection, level) -%}
<h{{ level }} id="{{ subsection.id }}"> {{subsection.name}}</h{{ level }}>
{{subsection.body}}

{% for subsubsection in subsection.subsections %}
{{ render_subsection(subsubsection, level+1) }}
{% endfor %}

{%- endmacro %}

{# specified top metadata #}
{% for subsections in api_metadata.subsections %}
		{%if subsections.name != api_metadata.subsections[0].name %}
            <section>
			    <h1 id="{{subsections.id}}">{{subsections.name}}</h1>
			    {{subsections.body}} 
            </section>
		{% endif %}
	
	{% for subsection in subsections.subsections %}
		{% if subsection.name in top_metadata %}
		  	<section>
				{{ render_subsection(subsection,2) }}
			</section>
		{% endif %}
	{% endfor%}


{# unespecified metadata #}


	{% for subsection in subsections.subsections %}
		{% if subsection.name not in top_metadata  and  subsection.name not in bottom_metadata and  subsection.name not in intro_metadata %}
			<section>
				{{ render_subsection(subsection,2) }}
			</section>
		{% endif %}
	{% endfor%}

{% endfor %}
