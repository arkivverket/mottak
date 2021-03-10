import json
import base64
import uuid
from app.connectors.mailgun.models import InvitasjonMelding, InvitasjonEmail

MAILGUN_DOMAIN = 'sandbox7cbdab032f7b4321af274439b1f353a2.mailgun.org'
TO = ['kriwal@arkivverket.no']
BASE64_URL = 'dpldr://eyJyZWZlcmVuY2UiOiAiMThkZGVkYjYtYThjOC00ZTI4LWIzNTUtZmM4MDJlMzlhNTg4IiwgInVwbG9hZF91cmwiOiAiaHR0cDovL3Rlc3Qubm8vIiwgInVwbG9hZF90eXBlIjogInRhciIsICJtZXRhIjogeyJpbnZpdGFzam9uX3V1aWQiOiAiZjM0NGEyODAtODQ0OS00ZjM5LWE3ZTktYzllMWI4NTg1MGE0In19'
TITTEL = 'Arkivgeneratorkomisjonen -- Et sikkelig bra arkiv'
_UUID = uuid.UUID('38da4005-92de-4aea-81ac-2262f90d0f5b')


EXAMPLE_MELDING = {"reference": "18ddedb6-a8c8-4e28-b355-fc802e39a588",
                   "uploadUrl": "http://test.no/",
                   "uploadType": "tar",
                   "meta": {"invitasjonEksternId": "4480d16c-267d-4051-aaea-fd5384895b2b"}}

EXAMPLE_EMAIL = {'subject': 'Invitasjon til opplastning',
                 'to': ['kriwal@arkivverket.no'],
                 'from': 'Mottak Digitalarkivet <donotreply@sandbox7cbdab032f7b4321af274439b1f353a2.mailgun.org>',
                 'text': 'Du mottar denne eposten fordi du har bestilt lenke til opplasting i Digitalarkivet. Det gjelder opplasting av følgende arkiv:\n\nTittel: Arkivgeneratorkomisjonen -- Et sikkelig bra arkiv\nObject id: 38da4005-92de-4aea-81ac-2262f90d0f5b\n\nDersom du ikke har bestilt lenke for opplasting kan du se bort fra denne eposten.\n\nTrinnvis beskrivelse av hvordan du laster opp et arkiv:\n- Siste versjon av program for å laste opp arkivuttrekk finnes her: https://uploader.digitalisering.arkivverket.no\n- Start applikasjonen\n- Trykk på invitasjons url’en i slutten av eposten (starter med dpldr://)\n- Velg tar fila som skal lastes opp\n\nInvitasjonslenken:\ndpldr://eyJyZWZlcmVuY2UiOiAiMThkZGVkYjYtYThjOC00ZTI4LWIzNTUtZmM4MDJlMzlhNTg4IiwgInVwbG9hZF91cmwiOiAiaHR0cDovL3Rlc3Qubm8vIiwgInVwbG9hZF90eXBlIjogInRhciIsICJtZXRhIjogeyJpbnZpdGFzam9uX3V1aWQiOiAiZjM0NGEyODAtODQ0OS00ZjM5LWE3ZTktYzllMWI4NTg1MGE0In19\n',
                 'html': 'Du mottar denne eposten fordi du har bestilt lenke til opplasting i Digitalarkivet. Det gjelder opplasting av følgende arkiv:\n<table style="text-align:left">\n    <tr>\n        <th>Tittel:</th>\n        <td>Arkivgeneratorkomisjonen -- Et sikkelig bra arkiv</td>\n    </tr>\n    <tr>\n        <th>Object id:</th>\n        <td>38da4005-92de-4aea-81ac-2262f90d0f5b</td>\n    </tr>\n<table>\n<br>\nDersom du ikke har bestilt lenke for opplasting kan du se bort fra denne eposten.\n<br>\n<br>\n\nTrinnvis beskrivelse av hvordan du laster opp et arkiv:\n<br>\n<ul>\n    <li>Siste versjon av program for å laste opp arkivuttrekk finnes her: <a href=https://uploader.digitalisering.arkivverket.no>https://uploader.digitalisering.arkivverket.no</a></li>\n    <li>Start applikasjonen</li>\n    <li>Trykk på invitasjonslenken i slutten av eposten (starter med dpldr://)</li>\n    <li>Velg tar fila som skal lastes opp</li>\n</ul>\n\nInvitasjonslenken:\n<br>\n<a href=dpldr://eyJyZWZlcmVuY2UiOiAiMThkZGVkYjYtYThjOC00ZTI4LWIzNTUtZmM4MDJlMzlhNTg4IiwgInVwbG9hZF91cmwiOiAiaHR0cDovL3Rlc3Qubm8vIiwgInVwbG9hZF90eXBlIjogInRhciIsICJtZXRhIjogeyJpbnZpdGFzam9uX3V1aWQiOiAiZjM0NGEyODAtODQ0OS00ZjM5LWE3ZTktYzllMWI4NTg1MGE0In19>dpldr://eyJyZWZlcmVuY2UiOiAiMThkZGVkYjYtYThjOC00ZTI4LWIzNTUtZmM4MDJlMzlhNTg4IiwgInVwbG9hZF91cmwiOiAiaHR0cDovL3Rlc3Qubm8vIiwgInVwbG9hZF90eXBlIjogInRhciIsICJtZXRhIjogeyJpbnZpdGFzam9uX3V1aWQiOiAiZjM0NGEyODAtODQ0OS00ZjM5LWE3ZTktYzllMWI4NTg1MGE0In19</a>\n'}


def test_invitasjon_melding_as_base64_url():
    """
    GIVEN   static input data to InvitasjonMelding
    WHEN    calling the method as_base64_url()
    THEN    verify that the correct base64 encoded url is returned
    """
    expected = _as_base64_url(EXAMPLE_MELDING)
    melding = InvitasjonMelding(uuid.UUID(EXAMPLE_MELDING['reference']), EXAMPLE_MELDING['uploadUrl'],
                                uuid.UUID(EXAMPLE_MELDING['meta']['invitasjonEksternId']),
                                EXAMPLE_MELDING['uploadType'])
    assert expected == melding.as_base64_url()


def test_mailgun_email():
    """
    GIVEN   static input data to MailgunEmail
    WHEN    calling the method as_data()
    THEN    verify that the correct dictionary is returned
    """
    email = InvitasjonEmail(MAILGUN_DOMAIN, TO, _UUID, TITTEL, BASE64_URL)
    print(email.as_data())
    assert EXAMPLE_EMAIL == email.as_data()


def _as_base64_url(data: dict) -> str:
    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')
    return 'dpldr://' + str(base64.b64encode(json_bytes), 'utf-8')
