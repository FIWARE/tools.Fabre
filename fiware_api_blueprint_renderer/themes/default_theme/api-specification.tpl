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
{% set intro_metadata = ["Copyright", "Abstract", "Status", "Status of this document", "Editors", "Versions", "License"]%}
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
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/monokai.css">
    <script src="js/highlight.pack.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    <script src="js/jquery.min.js"></script>
    <script src="js/toc-resize.js"></script>

    <link rel="stylesheet" type="text/css" href="css/api-specification.css"> 
    {%- if is_PDF %}
      <link rel="stylesheet" type="text/css" href="css/api-specification-pdf.css">
    {%- endif %}
    {%- for metadatum in metadata %}
      {%- if metadatum.name.upper() == 'CSS' %}
        <link rel="stylesheet" type="text/css" href="{{ metadatum.value }}"> 
      {%- endif %}
      {%- if metadatum.name.upper() == 'CSS-PDF' and is_PDF %}
        <link rel="stylesheet" type="text/css" href="{{ metadatum.value }}"> 
      {%- endif %}
    {%- endfor %}
    
</head>
<body id="respecDocument" class="h-entry">
<div class="container">

{% if not is_PDF %}
  <div id="TOC-container">
    {% include "fragments/toc.tpl" %}
  </div>
  {% endif %}


  <div id="API-content">
  {% if not is_PDF %}
    {% include "fragments/intro.tpl"%}
  {% endif %}


    {# API summary#}
    {% include "fragments/api-summary.tpl"%}

    {#  API top metadata #}
    {% include "fragments/top_metadata.tpl" %}

    {% if data_structures | contains_common_payload_definitions %}
      {# Common payload #}
      {% from 'fragments/common_payload.tpl' import renderPayloadAttributes %}
      
      <section id="common-payload-definition">
      <h2>Common Payload Definition</h2>

      {% for data_structure_name, data_structure in data_structures.iteritems() %}
          {% if data_structure_name != "REST API" and data_structure['is_common_payload'] %}
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
{% if is_PDF %}
<script type="text/javascript">
  function fix_links_class(){
     var links = document.getElementsByTagName("a");
     console.log(links);

     for (var i=0; i < links.length; i++ )
     {
      link = links[i];
      if ( link.textContent.indexOf(link.getAttribute('href')) > -1 )
          link.className= link.className + " selfContainedLink";
     }
  }
  
  fix_links_class();
</script>
{% endif %}
</html>
