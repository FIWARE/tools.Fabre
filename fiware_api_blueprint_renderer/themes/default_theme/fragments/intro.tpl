{%set title_doc = api_metadata.subsections[0].name %}
{% for metadata_value in metadata %}
	{% if metadata_value.name == "TITLE" %}
		{%set title_doc = metadata_value.value %}
	{%endif%}
{% endfor %}

<h1>{{title_doc}} </h1>


{% for metadata_value in metadata %}
	{% if metadata_value.name == "DATE" %}
		<span class="dateLabel">DATE:</span> <span class="dateValue"> {{ metadata_value.value }} </span>
	{%endif%}
{% endfor %}


{% for metadata_value in metadata %}
	{% if metadata_value.name == "HOST" %}
		{%set HOST =  metadata_value.value %}
		<dl>
		{% for metadata_value_aux in metadata %}
			{% if metadata_value_aux.name == "VERSION" %}
				<dt class="versionLabel">This version:</dt> 
				<dd class="versionValue"> <a href="{{metadata_value.value}}{{ metadata_value_aux.value }}">
					{{metadata_value.value}}{{ metadata_value_aux.value }}</a> </dd>
			{%endif%}
		{% endfor %}

		{% for metadata_value_aux in metadata %}
			{% if metadata_value_aux.name == "PREVIOUS_VERSION" %}
				<dt class="versionLabel">Previous version:</dt> 
				<dd class="versionValue"> <a href="{{metadata_value.value}}{{ metadata_value_aux.value }}">
					{{metadata_value.value}}{{ metadata_value_aux.value }}
				</a> </dd>
			{%endif%}
		{% endfor %}

		<dt class="versionLabel">Latest ersion:</dt> 
		<dd class="versionValue"> <a href="{{metadata_value.value}}latest">{{metadata_value.value}}latest</a> </dd>


		</dl>
	{%endif%}
{% endfor %}

{# 
{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Versions" %}
		<h2 id="{{subsection.id}}">Versions</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}
#}
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
{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Abstract" %}
		<h2 id="{{subsection.id}}">Abstract</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}


{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Status" or subsection.name == "Status of this document" %}
		<h2 id="{{subsection.id}}">Status of this document</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}
<hr>
