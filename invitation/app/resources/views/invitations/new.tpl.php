{% extends:'body' %}

{% block:content %}
<h2>Opprett ny opplasting</h2>
<hr>
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
