{% macro slug( id ) %}{{ id | lower | replace(' ', '_') }}{% endmacro %}
{% set top_metadata = ["Introduction", "Concepts", "Terminology"] %}
{% set bottom_metadata = ["Examples", "Acknowledgements", "References"] %}
{% set intro_metadata = ["Abstract", "Status", "Status of this document", "Editors", "Versions"]%}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ name }}</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">

    <!--
    
    <script src="js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/hightlight_default_theme.css">
    <link rel="stylesheet" href="css/monokai_sublime.css" type="text/css"> -->
    <link rel="stylesheet" href="css/idea.css">
    <script src="js/highlight.pack.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>

    <script src="js/jquery-1.11.3.min.js"></script>
    <!--<script src="js/TOC.js"></script>-->
    
    <link rel="stylesheet"href="css/w3c.css">
    <link rel="stylesheet" type="text/css" href="css/api-specification.css"> 

    
</head>
<body id="respecDocument" class="h-entry">

{% include "fragments/intro.tpl"%}

{% include "fragments/toc.tpl" %}
  <!-- API top metadata -->
  {% include "fragments/top_metadata.tpl" %}

<!-- API blueprint -->
    {% include "fragments/api_blueprint.tpl" %}

<!-- API bottom metadata -->
 {% include "fragments/bottom_metadata.tpl" %}
  
</body>
</html>
