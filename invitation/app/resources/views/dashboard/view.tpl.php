{% extends:'body' %}

{% block:content %}
	<h2>Opprett ny invitasjon til opplasting</h2>

	<hr>

	<a class="btn btn-primary btn-block" href="{{$_url->toRoute('invitations.new')}}" role="button">Opprett ny invitasjon til opplasting</a>

	<br>

	<h2>Nyeste opplastinger</h2>

	<hr>

	{% if($invitations->isEmpty()) %}
		{{view:'partials.alerts.info', ['message' => 'Det finnes ingen opplastinger.']}}
	{% else %}
		{{view:'invitations.partials.table'}}

		<br>

		<a class="btn btn-primary btn-block" href="{{$_url->toRoute('invitations')}}" role="button">Vis alle opplastinger</a>
	{% endif %}
{% endblock %}
