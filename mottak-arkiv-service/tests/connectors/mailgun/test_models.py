import json
import base64
import uuid
from app.connectors.mailgun.models import InvitasjonMelding, MailgunEmail

MAILGUN_DOMAIN = 'sandbox7cbdab032f7b4321af274439b1f353a2.mailgun.org'
TO = ['kriwal@arkivverket.no']
BASE64_URL = 'dpldr://eyJyZWZlcmVuY2UiOiAiMThkZGVkYjYtYThjOC00ZTI4LWIzNTUtZmM4MDJlMzlhNTg4IiwgInVwbG9hZF91cmwiOiAiaHR0cDovL3Rlc3Qubm8vIiwgInVwbG9hZF90eXBlIjogInRhciIsICJtZXRhIjogeyJpbnZpdGFzam9uX3V1aWQiOiAiZjM0NGEyODAtODQ0OS00ZjM5LWE3ZTktYzllMWI4NTg1MGE0In19'

EXAMPLE_MELDING = {"reference": "18ddedb6-a8c8-4e28-b355-fc802e39a588", "upload_url": "http://test.no/",
                   "upload_type": "tar", "meta": {"invitasjon_uuid": "4480d16c-267d-4051-aaea-fd5384895b2b"}}

EXAMPLE_EMAIL = {'from': f'Mottak <donotreply@{MAILGUN_DOMAIN}>', 'to': TO, 'subject': 'Invitasjon til opplasting av Arkivuttrekk', 'text': f'Opplastingslink for arkivuttrekk: {BASE64_URL}', 'html': f'Opplastingslink for arkivuttrekk: <a href={BASE64_URL}>{BASE64_URL}</a>'}


def test_invitasjon_melding_as_base64_url():
    """
    GIVEN   static input data to InvitasjonMelding
    WHEN    calling the method as_base64_url()
    THEN    verify that the correct base64 encoded url is returned
    """
    expected = _as_base64_url(EXAMPLE_MELDING)
    melding = InvitasjonMelding(uuid.UUID(EXAMPLE_MELDING['reference']), EXAMPLE_MELDING['upload_url'],
                                uuid.UUID(EXAMPLE_MELDING['meta']['invitasjon_uuid']), EXAMPLE_MELDING['upload_type'])
    assert expected == melding.as_base64_url()


def test_mailgun_email():
    """
    GIVEN   static input data to MailgunEmail
    WHEN    calling the method as_data()
    THEN    verify that the correct dictionary is returned
    """
    email = MailgunEmail(MAILGUN_DOMAIN, TO, BASE64_URL)
    assert EXAMPLE_EMAIL == email.as_data()


def _as_base64_url(data: dict) -> str:
    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')
    return 'dpldr://' + str(base64.b64encode(json_bytes), 'utf-8')
