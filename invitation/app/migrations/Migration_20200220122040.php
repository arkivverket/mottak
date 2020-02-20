<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200220122040 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Allow NULL in "invitations"."archive_type_id".';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ALTER COLUMN "archive_type_id" DROP NOT NULL,
			ALTER COLUMN "archive_type_id" SET DEFAULT NULL

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
