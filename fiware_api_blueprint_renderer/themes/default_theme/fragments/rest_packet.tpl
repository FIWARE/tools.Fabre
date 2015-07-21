{% macro rest_packet_body_div_id() %}{{ slug( action.name ) }}_{{ packet_type }}_{{ loop_index }}_body{% endmacro %}
<div class="rest-packet-div">
    <div class="container">
        <div class="col-md-10">
            <h5>{{ packet_type }}: {{ rest_packet.name }}</h5>
        </div>
        <div class="col-md-2">
            <a href="#{{ rest_packet_body_div_id() }}" class="btn btn-default" data-toggle="collapse">Toggle details</a>
        </div>
    </div>

    <div id="{{ rest_packet_body_div_id() }}" class="collapse action-div-body">
        <p>{{ rest_packet.description }}<p>

        {% if rest_packet.headers | length > 0 %}
	        <p>Headers</p>
	        <pre><code>{% for header in rest_packet.headers %}{{ header.name }}: {{ header.value | e }}
{% endfor %}</code></pre>
        {% endif %}

        {% if rest_packet.body | length > 0 %}
            <p>Body</p>
            <pre><code>{{ rest_packet.body }}</code></pre>
        {% endif %}

        {% set packet_contents = rest_packet.content %}
        {% include "fragments/rest_packet_contents.tpl" %}

        {% if rest_packet.schema | length > 0 %}
            <p>Schema</p>
            <pre><code>{{ rest_packet.schema }}</code></pre>
        {% endif %}
    </div>
</div>
