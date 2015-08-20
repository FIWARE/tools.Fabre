{# Deprecated, use parameters definition instead. Will be removed in further versions #}
{# Action parameters #}    
{% if parameters|length > 0 %}
	<div class="col-md-12 no-padding">       
		<table class="action-parameters-table">
		<caption>{{ parameters_table_caption }}</caption>
		<tr>
		    <th class="action-parameters-th">Name</th>
		    <th class="action-parameters-th">Required</th>
		    <th class="action-parameters-th">Type</th>
		    <th class="action-parameters-th">Description</th>
		</tr>
		{% for parameter in parameters %}
		<tr>
		    <td class="action-parameters-th">{{ parameter.name }}</td>
		    <td class="action-parameters-th">{{ parameter.required }}</td>
		    <td class="action-parameters-th">{{ parameter.type }}</td>
		    <td class="action-parameters-th">{{ parameter.description }}</td>
		</tr>
		{% endfor %}
		</table>
	</div>
{% endif %}
