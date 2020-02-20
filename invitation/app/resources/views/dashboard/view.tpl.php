{% extends:'body' %}

{% block:content %}

<h2>Opprett ny opplasting</h2>

<hr>

<a class="btn btn-primary btn-block" href="{{$_url->toRoute('invitations.new')}}" role="button">Opprett ny opplasting</a>

<br>

<h2>Nyeste opplastinger</h2>

<hr>

{% if($uploads->isEmpty()) %}
	{{view:'partials.alerts.info', ['message' => 'Det finnes ingen opplastinger.']}}
{% else %}
	<div class="table-responsive">
		<table class="table table-bordered table-hover">
			<thead>
				<tr>
					<th scope="col">UUID</th>
					<th scope="col">Dato</th>
					<th scope="col">Bruker</th>
					<th scope="col">Type</th>
					<th scope="col">Størrelse</th>
					<th scope="col">Status</th>
					<th scope="col">Handlinger</th>
				</tr>
			</thead>
			<tbody>
				{% foreach($uploads as $upload) %}
					<tr {% if(!$upload->archiveType) %}class="alert-warning"{% endif %}>
						<td>{{$upload->uuid}}</td>
						<td>{{$upload->created_at->format('Y-m-d H:i:s')}}</td>
						<td></td>
						<td>{{$upload->archiveType->type, default: 'Ukjent'}}</td>
						<td></td>
						<td></td>
						<td></td>
					</tr>
				{% endforeach %}
			</tbody>
		</table>
	</div>

	<br>

	<a class="btn btn-primary btn-block" href="{#{$_url->toRoute('invitations.list')}#}" role="button">Vis alle opplastinger</a>
{% endif %}

{% endblock %}
