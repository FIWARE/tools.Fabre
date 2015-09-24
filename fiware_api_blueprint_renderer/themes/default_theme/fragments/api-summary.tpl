
<nav class="api-summary">
<h1 id="api-summary"> API Summary </h1>
    <ul>

{# API #}
    {% for resourceGroup in resourceGroups %}

        <li>
            {% if resourceGroup.name|length > 1 %}
                <a href="#{{ gen_resource_group_id( resourceGroup.name ) }}" title = "{{ resourceGroup.name }}">{{ resourceGroup.name }}</a>
            {% else %}
                <a href="#default_group" title = "Default">Default</a>
            {% endif %}
            <ul>
              {% for resource in resourceGroup.resources %}
                {% if resource.ignoreTOC %}
                    {% for action in resource.actions %}
                        {% if action.name %}
                            <li>
                                <a href="#{{ action.id }}" title = "{{action.method}} - {{ action.name }}"><span class="actionMethod">{{action.method}}</span> - {{ action.name  }}
                                {% if action.attributes.uriTemplate %}
                                    [{{ action.attributes.uriTemplate }}]
                                {% else %}
                                    {% if resource.uriTemplate %}
                                        [{{resource.uriTemplate}}]
                                    {% endif %}
                                {% endif %}
                                </a>
                            </li>
                        {% else %}
                            {% if action.attributes.uriTemplate %}
                                <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ action.attributes.uriTemplate }}"><span class="actionMethod">{{action.method}}</span> - {{ action.attributes.uriTemplate }}  </a></li>
                            {% else %}
                                <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ resource.uriTemplate }}"><span class="actionMethod">{{action.method}}</span> - {{ resource.uriTemplate }} </a></li>
                            {% endif %}

                        {% endif %}
                        
                    {% endfor %}
                {% else %}
                    <li>
                        <a href="#{{ resource.id }}" title = "Resource {{ resource.name }}">
                        {% if resource.name %}
                            {{ resource.name }}
                        {% else %}
                            {{resource.uriTemplate}}
                        {% endif %}
                        </a>
                        <ul class="toc  ">
                        {% for action in resource.actions %}
                            {% if action.name %}
                                <li>
                                    <a href="#{{ action.id }}" title ="{{action.method}} - {{ action.name }}"><span class="actionMethod">{{action.method}}</span> - {{ action.name }}
                                    {% if action.attributes.uriTemplate %}
                                        [{{ action.attributes.uriTemplate }}]
                                    {% else %}
                                        {% if resource.uriTemplate %}
                                            [{{resource.uriTemplate}}]
                                        {% endif %}
                                    {% endif %}
                                    </a>
                                </li>
                            {% else %}
                                {% if action.attributes.uriTemplate %}
                                    <li><a href="#{{ action.id }}" title ="{{action.method}} - {{ action.attributes.uriTemplate }}"><span class="actionMethod">{{action.method}}</span> - {{ action.attributes.uriTemplate  }}</a></li>
                                {% else %}
                                    <li><a href="#{{ action.id }}" title ="{{action.method}}"><span class="actionMethod">{{action.method}}</span></a></li>
                                {% endif %}
                            {% endif %}

                        {% endfor %}
                        </ul>
                    </li>
                {% endif %}
              {% endfor %}
            </ul>
        </li>
      {% endfor %}

    </ul>
</nav>