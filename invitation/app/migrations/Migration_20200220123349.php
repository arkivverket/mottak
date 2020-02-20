<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200220123349 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Set the default value of "invitations"."object_name" to NULL.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ALTER COLUMN "object_name" SET DEFAULT NULL
		');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		// Don't roll back
	}
}
