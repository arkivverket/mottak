<div class="table-responsive">
	<table class="table table-bordered table-hover">
		<thead>
			<tr>
				<th scope="col">Arkiv</th>
				<th scope="col">Avgiver</th>
				<th scope="col">Sist endret</th>
				<th scope="col">Bruker</th>
				<th scope="col">Type</th>
				<th scope="col">Status</th>
				<th scope="col">Handlinger</th>
			</tr>
		</thead>
		<tbody>
			{% foreach($invitations as $invitation) %}
				<tr {% if(!$invitation->archiveType) %}class="alert-warning"{% endif %}>
					<td>
						<a href="{{$_url->toRoute('invitations.view', ['id' => $invitation->id])}}">
							{{$invitation->archive, default: 'Mangler navn'}}
						</a>
						<hr>
						<code>{{$invitation->uuid}}</code>
					</td>
					<td class="align-middle">{{$invitation->name}}</td>
					<td class="align-middle">{{$invitation->updated_at->format('Y-m-d H:i:s')}}</td>
					<td class="align-middle"></td>
					<td class="align-middle">{{$invitation->archiveType->type, default: 'Ukjent'}}</td>
					<td class="align-middle">{{$invitation->status, default: 'Ukjent'}}</td>
					<td class="align-middle"></td>
				</tr>
			{% endforeach %}
		</tbody>
	</table>
</div>
