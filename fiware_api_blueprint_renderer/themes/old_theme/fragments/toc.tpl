<div id="toc">
    <ul>
        <li class="extended_menu">
        <a href="#api-name">{{ name }}</a>
        <ul>
                <li><a href="#editors">Editors</a></li>
                <li><a href="#contributors">Contributors</a></li>
                <li><a href="#acknowledgements">Acknowledgements</a></li>
                <li><a href="#status">Status</a></li>
                <li><a href="#conformance">Conformance</a></li>
                <li>
                    <a href="#specification">Specification</a>
                    <ul>
                        <li><a href="#introduction">Introduction</a></li>
                        <li><a href="#terminology">Terminology</a></li>
                        <li><a href="#concepts">Concepts</a></li>
        	          {% for resourceGroup in resourceGroups %}
        	            <li>
                            <a href="#{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</a>
                            <ul>
        		              {% for resource in resourceGroup.resources %}
                               	<li>
                                    <a href="#{{ slug( resource.name ) }}">{{ resource.name }}</a>
                                    <ul>
        		                    {% for action in resource.actions %}
                                        <li><a href="#{{ slug( action.name ) }}">{{ action.name }}</a></li>
                                    {% endfor %}
                                    </ul>
                                </li>
                              {% endfor %}
                            </ul>
                        </li>
                      {% endfor %}
                           
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
</div>
