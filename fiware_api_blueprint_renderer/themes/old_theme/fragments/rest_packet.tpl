{% macro rest_packet_body_div_id() %}{{ slug( action.name ) }}_{{ packet_type }}_{{ loop_index }}_body{% endmacro %}
<div class="rest-packet-div col-md-12">
    <div class="row">
        <div class="col-md-10">
            <h5>{{ packet_type }} {{ rest_packet.name }}</h5>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            {% set packet_contents = rest_packet.content %}
            {% include "fragments/rest_packet_contents.tpl" %}
        </div>
    </div>

    <div class="row">
        <div class="col-md-12 toggle-button">
            <a href="#{{ rest_packet_body_div_id() }}" class="btn btn-default" data-toggle="collapse">Show example</a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div id="{{ rest_packet_body_div_id() }}" class="collapse action-div-body">
                <p>{{ rest_packet.description }}</p>

                {% if rest_packet.headers | length > 0 %}
        	        <p>Headers</p>
                    {% set headersStr = [] %}
                    {% for header in rest_packet.headers %}
                        {% if headersStr.append( header.name + ": " + header.value ) %}{% endif %}
                    {% endfor %}

        	        <pre><code>{{ headersStr | join( "\n" ) | e }}</code></pre>
                {% endif %}

                {% if rest_packet.body | length > 0 %}
                    <p>Body</p>
                    <pre><code>{{ rest_packet.body }}</code></pre>
                {% endif %}

                {% if rest_packet.schema | length > 0 %}
                    <p>Schema</p>
                    <pre><code>{{ rest_packet.schema }}</code></pre>
                {% endif %}
            </div>
        </div>
    </div>
</div>
