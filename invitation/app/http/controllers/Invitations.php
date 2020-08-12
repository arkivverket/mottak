<?php

namespace app\http\controllers;

use app\models\ArchiveType;
use app\models\Invitation;
use app\models\MetsFile;
use mako\http\exceptions\NotFoundException;
use mako\http\response\senders\Redirect;
use mako\http\routing\Controller;
use mako\validator\input\traits\InputValidationTrait;
use Symfony\Component\Mailer\Bridge\Mailgun\Transport\MailgunHttpTransport;
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mime\Email;
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
	public function list(): string
	{
		$invitations = Invitation::descending('id')->paginate();

		return $this->view->render('invitations.list',
		[
			'invitations' => $invitations,
		]);
	}

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

			$contents = str_replace("\xEF\xBB\xBF", '', file_get_contents($filePath)); // Strip BOM(s)

			$xml = simplexml_load_string(str_replace(['<mets:', '</mets:'], ['<', '</'], $contents));

			// Find the UUID and checksum

			$uuid = str_replace('UUID:', '', (string) $xml->attributes()['OBJID']);

			$archive = (string) $xml->attributes()['LABEL'];

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

			return [$contents, compact('name', 'email', 'uuid', 'archive', 'checksum')];
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
			'name'     => ['optional', 'max_length(255)'],
			'email'    => ['optional', 'email', 'max_length(255)'],
			'uuid'     => ['required', 'uuid', 'unique("invitations","uuid")'],
			'checksum' => ['required', 'exact_length(64)'],
			'archive'  => ['required', 'max_length(255)'],
		]);

		$invitation = new Invitation;

		$invitation->name         = $input['name'];
		$invitation->email        = $input['email'];
		$invitation->uuid         = $input['uuid'];
		$invitation->checksum     = $input['checksum'];
		$invitation->archive      = $input['archive'];

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
	public function view(int $id): string
	{
		$invitation = Invitation::get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		return $this->view->render('invitations.view',
		[
			'invitation' => $invitation,
		]);
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

	/**
	 *
	 */
	protected function buildUrl(Invitation $invitation): string
	{
		return 'dpldr://' . base64_encode(json_encode
		([
			'reference'  => $invitation->uuid,
			'uploadUrl'  => getenv('UPLOAD_URL'),
			'uploadType' => 'tar',
			'meta'       => ['invitation_id' => $invitation->id],
		]));
	}

	/**
	 *
	 */
	protected function sendEmail(string $recipient, string $url): void
	{
		$email = new Email;

		$email->to($recipient);

		$email->from('donotreply@' . getenv('MAILGUN_DOMAIN'));

		$email->subject('Invitasjon');

		$email->text($url);

		$email->html("<a href='{$url}'>{$url}</a>");

		$transport = new MailgunHttpTransport(getenv('MAILGUN_API_KEY'), getenv('MAILGUN_DOMAIN'));

		$mailer = new Mailer($transport);

		$mailer->send($email);
	}

	/**
	 *
	 */
	public function update(int $id): Redirect
	{
		$invitation = Invitation::get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		$isNewInvitation = $invitation->archive_type_id === null;

		$input = $this->validate($this->request->getData()->all(),
		[
			'name'            => ['required'],
			'email'           => ['required', 'email'],
			'archive_type_id' => ['required', 'exists("archive_types","id")'],
			'is_sensitive'    => ['required', 'in(["0","1"])'],
		]);

		$invitation->archive_type_id = $input['archive_type_id'];
		$invitation->is_sensitive    = $input['is_sensitive'] === '1' ? true : false;
		$invitation->name            = $input['name'];
		$invitation->email           = $input['email'];

		$invitation->save();

		if($isNewInvitation)
		{
			$this->sendEmail($invitation->email, $this->buildUrl($invitation));
		}

		return $this->redirectResponse('invitations.receipt', ['id' => $invitation->id]);
	}

	/**
	 *
	 */
	public function receipt(int $id): string
	{
		$invitation = Invitation::isNotNull('archive_type_id')->get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		return $this->view->render('invitations.receipt',
		[
			'invitation' => $invitation,
			'url'        => $this->buildUrl($invitation),
		]);
	}
}
