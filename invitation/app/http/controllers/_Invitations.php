<?php

namespace app\http\controllers;

use app\http\input\CreateInput;
use app\http\input\XmlInput;
use app\models\ArchiveType;
use app\models\Invitation;
use mako\http\exceptions\NotFoundException;
use mako\http\response\senders\Redirect;
use mako\http\routing\Controller;
use mako\validator\input\traits\InputValidationTrait;
use mako\view\ViewFactory;
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
	public function start(ViewFactory $view): string
	{
		return $view->render('invitations.xml');
	}

	/**
	 *
	 */
	public function parseXml(): Redirect
	{
		try
		{
			$input = $this->validate(XmlInput::class);

			$xml = file_get_contents($input['archive']->getRealPath());

			$xml = simplexml_load_string(str_replace(['<mets:', '</mets:'], ['<', '</'], $xml));

			// Find the UUID and checksum

			$uuid = str_replace('UUID:', '', (string) $xml->attributes()['OBJID']);

			$checksum = (string) $xml->fileSec->fileGrp->file->attributes()['CHECKSUM'];

			$name = $email = null;

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

			$archive = compact('uuid', 'checksum', 'name', 'email');
		}
		catch(Throwable $e)
		{
			$archive = false;

			$this->logger->error($e->getMessage(), ['exception' => $e]);
		}

		// Flash the data and redirect to the next form

		$this->session->putFlash('archive', $archive);

		return $this->redirectResponse('invitations.create');
	}

	/**
	 *
	 */
	public function create(): string
	{
		$input = $this->session->getFlash('archive');

		return $this->view->render('invitations.create',
		[
			'input'           => $input === false ? null : $input,
			'failed_to_parse' => $input === false,
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
	public function store(): Redirect
	{
		$input = $this->validate(CreateInput::class);

		try
		{
			$this->database->connection()->beginTransaction();

			$invitation = new Invitation;

			$invitation->archive_type_id = $input['archive_type_id'];

			$invitation->uuid = $input['uuid'];

			$invitation->checksum = $input['checksum'];

			$invitation->is_sensitive = $input['is_sensitive'] === '1' ? true : false;

			$invitation->name = $input['name'];

			$invitation->email = $input['email'];

			$invitation->save();

			$this->sendEmail($invitation->email, $this->buildUrl($invitation));

			$this->database->connection()->commitTransaction();
		}
		catch(Throwable $e)
		{
			$this->database->connection()->rollBackTransaction();

			throw $e;
		}

		return $this->redirectResponse('invitations.receipt', ['id' => $invitation->id]);
	}

	/**
	 *
	 */
	public function receipt(string $id): string
	{
		$invitation = Invitation::get($id);

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
