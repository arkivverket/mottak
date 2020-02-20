<?php

namespace app\http\controllers;

use app\models\Invitation;
use mako\database\midgard\ResultSet;
use mako\http\routing\Controller;

/**
 *
 */
class Dashboard extends Controller
{
	/**
	 *
	 */
	protected function getLastUploads(): ResultSet
	{
		return Invitation::including(['archiveType'])->descending('id')->limit(10)->all();
	}

	/**
	 *
	 */
	public function view(): string
	{
		return $this->view->render('dashboard.view',
		[
			'invitations' => $this->getLastUploads(),
		]);
	}
}
