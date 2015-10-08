{% set title_metadata = {} %}
{% for metadata_value in metadata %}
	{% if metadata_value.name == "TITLE" %}
		{% do title_metadata.update(TITLE = metadata_value.value) %}
	{%endif%}
{% endfor %}

{% if "TITLE" in title_metadata %}
	<h1>{{ title_metadata['TITLE'] | e }} </h1>
{% else %}
	<h1>{{name | e}} </h1>
{% endif %}

{% for metadata_value in metadata %}
	{% if metadata_value.name == "DATE" %}
		<span class="dateLabel">DATE:</span> <span class="dateValue"> {{ metadata_value.value }} </span>
	{%endif%}
{% endfor %}

{% set version_sections = {} %}

{% for metadata_value in metadata %}
	{% if metadata_value.name == "SPEC_URL" %}
		{% do version_sections.update(SPEC_URL = metadata_value.value) %}
	{%endif%}
	{% if metadata_value.name == "VERSION" %}
		{% do version_sections.update(VERSION = metadata_value.value) %}
	{%endif%}
	{% if metadata_value.name == "PREVIOUS_VERSION" %}
		{% do version_sections.update({'PREVIOUS_VERSION':metadata_value.value}) %}
	{%endif%}
{% endfor %}

{% if "SPEC_URL" in version_sections and ("VERSION" in version_sections or "PREVIOUS_VERSION" in version_sections) %}
	<dl>
	{% if "VERSION" in version_sections %}
		<dt class="versionLabel">This version:</dt> 
		<dd class="versionValue"> <a href="{{version_sections['SPEC_URL']}}{{ version_sections['VERSION'] }}">
			{{version_sections['SPEC_URL']}}{{ version_sections['VERSION']|e }}
		</a> </dd>
	{%endif%}

	{% if "PREVIOUS_VERSION" in version_sections %}
		<dt class="versionLabel">Previous version:</dt> 
		<dd class="versionValue"> <a href="{{version_sections['SPEC_URL']}}{{ version_sections['PREVIOUS_VERSION'] }}">
			{{version_sections['SPEC_URL']}}{{ version_sections['PREVIOUS_VERSION']|e }}
		</a> </dd>
	{%endif%}

	<dt class="versionLabel">Latest version:</dt> 
	<dd class="versionValue"> <a href="{{SPEC_URL}}latest">{{version_sections['SPEC_URL']}}latest</a> </dd>

	</dl>
{%endif%}

{% set source_sections = {} %}

{% for metadata_section in metadata %}
  {% if metadata_section.name == "APIARY_PROJECT" %}
    {% do source_sections.update(APIARY_PROJECT = metadata_section.value) %}
  {%endif%}
  {% if metadata_section.name == "GITHUB_SOURCE" %}
    {% do source_sections.update(GITHUB_SOURCE = metadata_section.value) %}
  {%endif%}
{% endfor %}

{% if "APIARY_PROJECT" in source_sections or "GITHUB_SOURCE" in source_sections %}
  <div id="top-source-buttons">
  	{% if "APIARY_PROJECT" in source_sections %}
    	<a target="_blank" href="http://docs.{{source_sections['APIARY_PROJECT'] }}.apiary.io/#reference">View in Apiary</a>
    {% endif %}
    {% if "GITHUB_SOURCE" in source_sections %}
    	<a target="_blank" href="{{source_sections['GITHUB_SOURCE'] }}">View in Github</a>
    {% endif %}
  </div>
{% endif %}

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
