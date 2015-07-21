<!-- Action parameters -->     
{% if parameters|length > 0 %}               
	<table class="action-parameters-table">
	<caption>Parameters</caption>
	<tr>
	    <th class="action-parameters-th">Name</th>
	    <th class="action-parameters-th">Default value</th>
	    <th class="action-parameters-th">Required</th>
	    <th class="action-parameters-th">Values</th>
	    <th class="action-parameters-th">Type</th>
	    <th class="action-parameters-th">Example</th>
	    <th class="action-parameters-th">Description</th>
	</tr>
	{% for parameter in parameters %}
	<tr>
	    <td class="action-parameters-th">{{ parameter.name }}</td>
	    <td class="action-parameters-th">{{ parameter.default }}</td>
	    <td class="action-parameters-th">{{ parameter.required }}</td>
	    <td class="action-parameters-th">
        {% for value in parameter['values'] %}
            {{ value.value }}, 
        {% endfor %}
        </td>
	    <td class="action-parameters-th">{{ parameter.type }}</td>
	    <td class="action-parameters-th">{{ parameter.example }}</td>
	    <td class="action-parameters-th">{{ parameter.description }}</td>
	</tr>
	{% endfor %}
	</table>
{% endif %}
