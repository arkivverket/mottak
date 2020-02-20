{% extends:'body' %}

{% block:content %}
	<h2>Opplastinger</h2>

	<hr>

	{{raw:$invitations->getPagination()->render('partials.pagination')}}

	{% if($invitations->isEmpty()) %}
		{{view:'partials.alerts.info', ['message' => 'Det finnes ingen opplastinger.']}}
	{% else %}
		{{view:'invitations.partials.table'}}
	{% endif %}

	{{raw:$invitations->getPagination()->render('partials.pagination')}}
{% endblock %}
