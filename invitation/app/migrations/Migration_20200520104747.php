<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200520104747 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Adds "archive" column to the "invitations" table.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ADD COLUMN "archive" VARCHAR(255)
		');

		$this->getConnection()->query
		('
			UPDATE "invitations" SET "archive" = \'\'
		');

		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ALTER COLUMN "archive" SET NOT NULL
		');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			DROP COLUMN "archive"
		');
	}
}
