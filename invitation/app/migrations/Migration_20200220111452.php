<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200220111452 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Allow NULL in "invitations"."name" and "invitations"."email" columns.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ALTER COLUMN "name" DROP NOT NULL,
			ALTER COLUMN "name" SET DEFAULT NULL,
			ALTER COLUMN "email" DROP NOT NULL,
			ALTER COLUMN "email" SET DEFAULT NULL

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
