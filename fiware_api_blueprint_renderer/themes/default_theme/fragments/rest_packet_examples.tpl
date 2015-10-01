{% macro rest_packet_body_div_id() %}{{ gen_action_id( action.name ) }}_{{ packet_type }}_{{ loop_index }}_body{% endmacro %}
{% macro rest_packet_mime(headers) -%}
    {% for header in headers %}
        {% if 'Content-Type'==header.name %}
            ({{ header.value }})
        {% endif %}
    {% endfor %}
{%- endmacro %}
<div class="rest-packet-div">

            <span class="packetType">{{ packet_type }} {{ rest_packet.name }}</span> {{rest_packet_mime(rest_packet.headers)}}
            
            
            {% set packet_contents = rest_packet.content %}
            {# Now show in definition #}
           {# {% include "fragments/rest_packet_contents.tpl" %} #}


 
            <div id="{{ rest_packet_body_div_id() }}" class=" action-div-body">
                <p>{{ rest_packet.description }}</p>

                {% if rest_packet.headers | length > 0 %}
        	         <div class= "header"><p>Headers</p></div>
                    {% set headersStr = [] %}
                    {% for header in rest_packet.headers %}
                        {% if headersStr.append( header.name + ": " + header.value ) %}{% endif %}
                    {% endfor %}

        	        <pre><code>{{ headersStr | join( "\n" ) | e }}</code></pre>
                {% endif %}

                {% if rest_packet.body | length > 0 %}
                    <div class= "header"><p>Body</p></div>
                    <pre><code>{{ rest_packet.body }}</code></pre>
                {% endif %}

                {% if rest_packet.schema | length > 0 %}
                    <div class= "header"><p>Schema</p></div>
                    <pre><code>{{ rest_packet.schema }}</code></pre>
                {% endif %}
            </div>
            
            
     
</div>
