<div id="toc">
    <ul>
        <li><a href="#api-name">{{ name }}</a></li>
        <li><a href="#editors">Editors</a></li>
        <li><a href="#contributors">Contributors</a></li>
        <li><a href="#acknowledgements">Acknowledgements</a></li>
        <li><a href="#status">Status</a></li>
        <li><a href="#conformance">Conformance</a></li>
        <li><a href="#specification">Specification</a></li>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#terminology">Terminology</a></li>
        <li><a href="#concepts">Concepts</a></li>
	    {% for resourceGroup in resourceGroups %}
	    <li><a href="#{{ slug( resourceGroup.name ) }}">{{ resourceGroup.name }}</a></li>
            <ul>
		    {% for resource in resourceGroup.resources %}
           		<li><a href="#{{ slug( resource.name ) }}">{{ resource.name }}</a></li>
                <ul>
		        {% for action in resource.actions %}
                    <li><a href="#{{ slug( action.name ) }}">{{ action.name }}</a></li>
                {% endfor %}
                </ul>
            {% endfor %}
            </ul>
        {% endfor %}
    </ul>
</div>
