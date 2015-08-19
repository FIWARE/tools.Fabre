{% macro slug( id ) %}{{ id | lower | replace(' ', '-') }}{% endmacro %}

{% macro gen_resource_group_id( resGroupName ) %}resource_group_{{ slug( resGroupName ) }}{% endmacro %}
{% macro gen_resource_id( resName ) %}resource_{{ slug( resName ) }}{% endmacro %}
{% macro gen_action_id( actionName ) %}action_{{ slug( actionName ) }}{% endmacro %}

{% macro gen_resource_group_example_id( resGroupName ) %}{{ gen_resource_group_id( resGroupName ) }}_example{% endmacro %}
{% macro gen_resource_example_id( resName ) %}{{ gen_resource_id( resName ) }}_example{% endmacro %}
