<?php

namespace app\http\controllers;

use app\models\ArchiveType;
use app\models\Invitation;
use app\models\MetsFile;
use mako\http\exceptions\NotFoundException;
use mako\http\response\senders\Redirect;
use mako\http\routing\Controller;
use mako\validator\input\traits\InputValidationTrait;
use Throwable;

/**
 *
 */
class Invitations extends Controller
{
	use InputValidationTrait;

	/**
	 *
	 */
	public function new(): string
	{
		return $this->view->render('invitations.new');
	}

	/**
	 *
	 */
	protected function parseXML(string $filePath): array
	{
		try
		{
			$name = $email = null;

			$contents = file_get_contents($filePath);

			$xml = simplexml_load_string(str_replace(['<mets:', '</mets:'], ['<', '</'], $contents));

			// Find the UUID and checksum

			$uuid = str_replace('UUID:', '', (string) $xml->attributes()['OBJID']);

			$checksum = (string) $xml->fileSec->fileGrp->file->attributes()['CHECKSUM'];

			// Try to find the submitter

			foreach($xml->metsHdr->agent as $agent)
			{
				$attributes = $agent->attributes();

				if((string) $attributes['OTHERROLE'] === 'SUBMITTER' && (string) $attributes['TYPE'] === 'INDIVIDUAL')
				{
					$name = (string) $agent->name;

					foreach($agent->note as $note)
					{
						if(strpos((string) $note, '@') !== false)
						{
							$email = (string) $note;
						}
					}

					break;
				}
			}

			return [$contents, compact('name', 'email', 'uuid', 'checksum')];
		}
		catch(Throwable $e)
		{
			$this->logger->error($e->getMessage(), ['exception' => $e]);

			return ['', []];
		}
	}

	/**
	 *
	 */
	public function create(): Redirect
	{
		// Validate form data and parse XML-file

		$input = $this->validate($this->request->getFiles()->all(),
		[
			'archive' => ['required', 'is_uploaded', 'mime_type(["application/xml", "text/xml"])'],
		]);

		[$xml, $data] = $this->parseXml($input['archive']->getRealPath());

		// Validate XML-data and create invitation

		$input = $this->validate($data,
		[
			'name'     => ['optional'],
			'email'    => ['optional', 'email'],
			'uuid'     => ['required', 'uuid', 'unique("invitations","uuid")'],
			'checksum' => ['required', 'exact_length(64)'],
		]);

		$invitation = new Invitation;

		$invitation->name     = $input['name'];
		$invitation->email    = $input['email'];
		$invitation->uuid     = $input['uuid'];
		$invitation->checksum = $input['checksum'];

		$invitation->save();

		$metsFile = new MetsFile;

		$metsFile->contents = $xml;

		$invitation->metsFile()->create($metsFile);

		// Redirect to edit form

		return $this->redirectResponse('invitations.edit', ['id' => $invitation->id]);
	}

	/**
	 *
	 */
	public function edit(int $id): string
	{
		$invitation = Invitation::get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		return $this->view->render('invitations.edit',
		[
			'invitation'      => $invitation,
			'archive_types'   => ArchiveType::ascending('type')->all(),
		]);
	}

	/*
	 *
	 */
	public function update(int $id): Redirect
	{
		$invitation = Invitation::get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		$input = $this->validate($this->request->getData()->all(),
		[
			'name'            => ['required'],
			'email'           => ['required', 'email'],
			'archive_type_id' => ['required', 'exists("archive_types","id")'],
			'is_sensitive'    => ['required', 'in(["0","1"])'],
		]);

		var_dump($input); exit;
	}
}
