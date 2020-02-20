<nav aria-label="Paginering">
	<ul class="pagination">
		{% if(isset($previous)) %}
			<li class="page-item"><a class="page-link" href="{{preserve:$first}}">Første</a></li>
			<li class="page-item"><a class="page-link" href="{{preserve:$previous}}">Forrige</a></li>
		{% endif %}
		{% foreach($pages as $page) %}
			{% if($page['is_current']) %}
				<li class="page-item active" aria-current="page"><a class="page-link" href="#">{{$page['number']}}</a></li>
			{% else %}
				<li class="page-item"><a class="page-link" href="{{preserve:$page['url']}}">{{$page['number']}}</a></li>
			{% endif %}
		{% endforeach %}
		{% if(isset($next)) %}
			<li class="page-item"><a class="page-link" href="{{preserve:$next}}">Neste</a></li>
			<li class="page-item"><a class="page-link" href="{{preserve:$last}}">Siste</a></li>
		{% endif %}
	</ul>
</nav>
