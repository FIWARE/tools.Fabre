{% for metadata_value in metadata %}
	{% if metadata_value.name == "TITLE" %}
		<h1>{{metadata_value.value}} </h1>
	{%endif%}
{% endfor %}

{% for metadata_value in metadata %}
	{% if metadata_value.name == "DATE" %}
		<span class="dateLabel">DATE:</span> <span class="dateValue"> {{ metadata_value.value }} </span>
	{%endif%}
{% endfor %}


{% for metadata_value in metadata %}
	{% if metadata_value.name == "HOST" %}
		{% set HOST = metadata_value.value %}
		<dl>
		{% for metadata_value_aux in metadata %}
			{% if metadata_value_aux.name == "VERSION" %}
				<dt class="versionLabel">This version:</dt> 
				<dd class="versionValue"> <a href="{{HOST}}{{ metadata_value_aux.value }}">
					{{HOST}}{{ metadata_value_aux.value }}</a> </dd>
			{%endif%}
		{% endfor %}

		{% for metadata_value_aux in metadata %}
			{% if metadata_value_aux.name == "PREVIOUS_VERSION" %}
				<dt class="versionLabel">Previous version:</dt> 
				<dd class="versionValue"> <a href="{{HOST}}{{ metadata_value_aux.value }}">
					{{HOST}}{{ metadata_value_aux.value }}
				</a> </dd>
			{%endif%}
		{% endfor %}

		<dt class="versionLabel">Latest version:</dt> 
		<dd class="versionValue"> <a href="{{HOST}}latest">{{HOST}}latest</a> </dd>


		</dl>
	{%endif%}
{% endfor %}

{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Editors" %}
		<h2 id="{{subsection.id}}">Editors</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}

{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Copyright" %}
		<h2 id="{{subsection.id}}">Copyright</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}

<hr>

{% if description %}
	<h2 id="abstract">Abstract</h2>
	{{description}}
{% else %}
	{% if api_metadata.subsections[0].body %}
	<h2 id="abstract">Abstract</h2>
		{{api_metadata.subsections[0].body}}
	{% endif %}
{%endif %}


{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Status" or subsection.name == "Status of this document" %}
		<h2 id="{{subsection.id}}">Status of this document</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}
<hr>
