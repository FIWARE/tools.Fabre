{% from 'fragments/id-generation-macros.tpl' import 
    slug, 
    gen_resource_id, 
    gen_action_id, 
    gen_resource_group_id, 
    gen_resource_group_example_id, 
    gen_resource_example_id,
    gen_apiary_link
%}

{% set top_metadata = ["Introduction", "Concepts", "Terminology"] %}
{% set bottom_metadata = ["Examples", "Acknowledgements", "References"] %}
{% set intro_metadata = ["Copyright", "Abstract", "Status", "Status of this document", "Editors", "Versions"]%}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ name }}</title>
    <link href="css/bootstrap-combined.no-icons.min.css" rel="stylesheet">
    <link href="css/font-awesome.css" rel="stylesheet">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/idea.css">
    <script src="js/highlight.pack.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>

    <link rel="stylesheet" type="text/css" href="css/api-specification.css"> 

    
</head>
<body id="respecDocument" class="h-entry">
<div class="container">
  <div id="TOC-container">
    {% include "fragments/toc.tpl" %}
  </div>
  <div id="API-content">
  {% include "fragments/intro.tpl"%}

    {#  API top metadata #}
    {% include "fragments/top_metadata.tpl" %}

    {% if data_structures|length > 1 %}
      {# Common payload #}
      {% from 'fragments/common_payload.tpl' import renderPayloadAttributes %}
      
      <section id="common-payload-definition">
      <h2>Common Payload Definition</h2>

      {% for data_structure_name, data_structure in data_structures.iteritems() %}
          {% if data_structure_name != "REST API" %}
              <h3>{{ data_structure_name }}</h3>
              {{ renderPayloadAttributes( data_structure['attributes'] ) }}
          {% endif %}
      {% endfor %}
      </section>
    {% endif %}

  {#  API blueprint #}
  <section id="API_specification">
      <h1>API Specification</h1>
      {% include "fragments/api_blueprint.tpl" %}
  </section>
  {#  API bottom metadata #}
   {% include "fragments/bottom_metadata.tpl" %}
    
    {#  References #}
    {%if reference_links|length > 0 %}
      <section id="references">
      <h1>References</h1>
          <ul>
              {% for link in reference_links %}
                  <li><a href="{{ link.url }}">{{ link.title }}</a></li>
              {% endfor %}
          </ul>
      </section>
    {% endif %}
  </div>
</div>
</body>
</html>
