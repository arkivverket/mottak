<div class="alert alert-danger alert-dismissible fade show" role="alert">
	<h4 class="alert-heading">Oisann!</h4>
	<hr>
	<ul>
	{% foreach($errors as $error) %}
		<li>{{$error}}</li>
	{% endforeach %}
	</ul>
	<button type="button" class="close" data-dismiss="alert" aria-label="Close">
		<span aria-hidden="true">&times;</span>
	</button>
</div>
