<h1>{{api_metadata.subsections[0].name}}</h1>


{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Versions" %}
		<h2 id="{{subsection.id}}">Versions</h2>
		{{subsection.body}}
	{%endif%}
{% endfor %}

{% for subsection in api_metadata.subsections[0].subsections %}
	{% if subsection.name == "Editors" %}
		<h2 id="{{subsection.id}}">Editors</h2>
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