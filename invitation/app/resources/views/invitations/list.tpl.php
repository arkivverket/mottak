{% extends:'body' %}

{% block:breadcrumb %}
	<nav aria-label="breadcrumb">
		<ol class="breadcrumb">
			<li class="breadcrumb-item"><a href="{{$_url->toRoute('dashboard.view')}}">Hjem</a></li>
			<li class="breadcrumb-item active" aria-current="page">Opplastinger</li>
		</ol>
	</nav>
{% endblock %}

{% block:content %}
	{{raw:$invitations->getPagination()->render('partials.pagination')}}

	{% if($invitations->isEmpty()) %}
		{{view:'partials.alerts.info', ['message' => 'Det finnes ingen opplastinger.']}}
	{% else %}
		{{view:'invitations.partials.table'}}
	{% endif %}

	{{raw:$invitations->getPagination()->render('partials.pagination')}}
{% endblock %}
