{% extends:'body' %}

{% block:breadcrumb %}
	<nav aria-label="breadcrumb">
		<ol class="breadcrumb">
			<li class="breadcrumb-item"><a href="{{$_url->toRoute('dashboard.view')}}">Hjem</a></li>
			<li class="breadcrumb-item"><a href="{{$_url->toRoute('invitations')}}">Opplastinger</a></li>
			<li class="breadcrumb-item active" aria-current="page">Opprett ny invitasjon til opplasting</li>
		</ol>
	</nav>
{% endblock %}

{% block:content %}
	<form method="POST" enctype="multipart/form-data">
		<div class="form-group">
			<label for="archiveFile">METS-fil</label>
			<div class="custom-file">
				<input type="file" name="archive" class="custom-file-input" id="archiveFile">
				<label class="custom-file-label" for="archiveFile">Velg fil</label>
			</div>
		</div>
		<button type="submit" class="btn btn-primary">Last opp</button>
	</form>

	<script>
	$('#archiveFile').on('change',function() {
		var fileName = $(this).val();
		$(this).next('.custom-file-label').html(fileName.replace('C:\\fakepath\\', ''));
	})
	</script>
{% endblock %}
