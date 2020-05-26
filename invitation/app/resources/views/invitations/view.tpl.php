{% extends:'body' %}

{% block:breadcrumb %}
	<nav aria-label="breadcrumb">
		<ol class="breadcrumb">
			<li class="breadcrumb-item"><a href="{{$_url->toRoute('dashboard.view')}}">Hjem</a></li>
			<li class="breadcrumb-item"><a href="{{$_url->toRoute('invitations')}}">Opplastinger</a></li>
			<li class="breadcrumb-item active" aria-current="page">Opplasting</li>
		</ol>
	</nav>
{% endblock %}

{% block:content %}
	<div class="card">
		<div class="card-header">
			{{$invitation->archive, default: 'Mangler navn'}}
		</div>
		<div class="card-body">
			<div class="table-responsive">
				<table class="table table-borderless table-hover mb-0">
					<tbody>
						<tr>
							<th scope="row" class="text-left">Opprettet</th>
							<td>{{$invitation->created_at->format('Y-m-d H:i:s')}}</td>
						</tr>
						<tr>
							<th scope="row" class="text-left">Sist endret</th>
							<td>{{$invitation->created_at->format('Y-m-d H:i:s')}}</td>
						</tr>
						<tr>
							<th scope="row" class="text-left">Avgiver</th>
							<td>{{$invitation->name}} (<a href="mailto:{{$invitation->email}}">{{$invitation->email}}</a>)</td>
						</tr>
						<tr>
							<th scope="row" class="text-left">Arkivtype</th>
							<td>{{$invitation->archiveType->type, default: 'Ukjent'}}</td>
						</tr>
						<tr>
							<th scope="row" class="text-left">UUID</th>
							<td><code>{{$invitation->uuid}}</code></td>
						</tr>
						<tr>
							<th scope="row" class="text-left">Sjekksum</th>
							<td><code>{{$invitation->checksum}}</code></td>
						</tr>
						<tr>
							<th scope="row" class="text-left">Status</th>
							<td>{{$invitation->status, default: 'Ukjent'}}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>

	<div id="log-entries">

	</div>
{% endblock %}
