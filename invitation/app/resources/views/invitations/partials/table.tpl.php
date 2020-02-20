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
			{% foreach($invitations as $invitation) %}
				<tr {% if(!$invitation->archiveType) %}class="alert-warning"{% endif %}>
					<td>{{$invitation->uuid}}</td>
					<td>{{$invitation->created_at->format('Y-m-d H:i:s')}}</td>
					<td></td>
					<td>{{$invitation->archiveType->type, default: 'Ukjent'}}</td>
					<td></td>
					<td></td>
					<td></td>
				</tr>
			{% endforeach %}
		</tbody>
	</table>
</div>
