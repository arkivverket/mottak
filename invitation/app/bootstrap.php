<?php

// This file gets included at the end of the application boot sequence

use mako\http\Request;
use mako\http\routing\URLBuilder;
use mako\view\ViewFactory;

if(!$app->isCommandLine())
{
	$app->getContainer()->get(ViewFactory::class)->autoAssign('*', function() use ($app)
	{
		return
		[
			'_url'   => $app->getContainer()->get(URLBuilder::class),
			'_route' => $app->getContainer()->get(Request::class)->getRoute(),
		];
	});
}
