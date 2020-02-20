<?php

use mako\http\routing\Routes;

/* @var \mako\http\routing\Routes $routes */

$routes->group(['namespace' => 'app\http\controllers', 'middleware' => ['security_headers', 'input_validation']], function(Routes $routes): void
{
	$routes->get('/', 'Dashboard::view', 'dashboard.view');

	$routes->group(['prefix' => 'invitations'], function(Routes $routes): void
	{
		/*$routes->get('/new', 'Invitations::start', 'invitations.new');

		$routes->post('/new', 'Invitations::parseXml');

		$routes->get('/create', 'Invitations::create', 'invitations.create');

		$routes->post('/create', 'Invitations::store');

		$routes->get('/receipt/{id}', 'Invitations::receipt', 'invitations.receipt')->patterns(['id' => '[0-9]+']);*/

		$routes->get('/new', 'Invitations::new', 'invitations.new');

		$routes->post('/new', 'Invitations::create');

		$routes->get('/edit/{id}', 'Invitations::edit', 'invitations.edit')->patterns(['id' => '[0-9]+']);

		$routes->post('/edit/{id}', 'Invitations::update')->patterns(['id' => '[0-9]+']);
	});
});
