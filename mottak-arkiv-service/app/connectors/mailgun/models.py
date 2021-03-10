import json
import base64
from uuid import UUID
from typing import List
from abc import ABC


class MailgunEmail(ABC):
    def __init__(self, subject: str, to: List[str], sender: str, body_text: str, body_html: str):
        self.__subject = subject
        self.__to = to
        self.__from = sender
        self.__text = body_text
        self.__html = body_html

    def as_data(self):
        """
        Creates a dict adhering to Mailguns expected data structure
        :return: a dict following Mailguns eexpected data structure
        """
        return {'subject': self.__subject, 'to': self.__to, 'from': self.__from, 'text': self.__text,
                'html': self.__html}


class InvitasjonMelding:
    """
    Creating invitasjon json object in expected structure for the archive-uploader
    """
    __url_prefix = 'dpldr://'

    def __init__(self, arkivuttrekk_obj_id: UUID, upload_url: str, invitasjon_ekstern_id: UUID, upload_type: str = 'tar'):
        self.reference = str(arkivuttrekk_obj_id)
        self.uploadUrl = upload_url
        self.uploadType = upload_type
        self.meta = {'invitasjonEksternId': str(invitasjon_ekstern_id)}

    def as_base64_url(self) -> str:
        """
        Base64 encodes the json object
        :return: a base64 encoded url as string
        """
        json_str = json.dumps(self.__dict__)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return self.__url_prefix + base64_str


class InvitasjonEmail(MailgunEmail):
    """
    Template class for sending upload links through Mailgun.
    """

    __subject = "Invitasjon til opplastning"

    def __init__(self, mailgun_domain: str, to: List[str], arkivuttrekk_obj_id: UUID, arkivuttrekk_tittel: str,
                 upload_url: str):
        super().__init__(self.__subject,
                         to,
                         f'Mottak Digitalarkivet <donotreply@{mailgun_domain}>',
                         InvitasjonEmail.__body_as_text(arkivuttrekk_obj_id, arkivuttrekk_tittel, upload_url),
                         InvitasjonEmail.__body_as_html(arkivuttrekk_obj_id, arkivuttrekk_tittel, upload_url))

    @staticmethod
    def __body_as_text(obj_id: UUID, tittel: str, upload_url: str) -> str:
        return f"""Du mottar denne eposten fordi du har bestilt lenke til opplasting i Digitalarkivet. Det gjelder opplasting av følgende arkiv:

Tittel: {tittel}
Object id: {obj_id}

Dersom du ikke har bestilt lenke for opplasting kan du se bort fra denne eposten.

Trinnvis beskrivelse av hvordan du laster opp et arkiv:
- Siste versjon av program for å laste opp arkivuttrekk finnes her: https://uploader.digitalisering.arkivverket.no
- Start applikasjonen
- Trykk på invitasjons url’en i slutten av eposten (starter med dpldr://)
- Velg tar fila som skal lastes opp

Invitasjonslenken:
{upload_url}
"""

    @staticmethod
    def __body_as_html(obj_id: UUID, tittel: str, upload_url: str) -> str:
        return f"""Du mottar denne eposten fordi du har bestilt lenke til opplasting i Digitalarkivet. Det gjelder opplasting av følgende arkiv:
<table style="text-align:left">
    <tr>
        <th>Tittel:</th>
        <td>{tittel}</td>
    </tr>
    <tr>
        <th>Object id:</th>
        <td>{obj_id}</td>
    </tr>
<table>
<br>
Dersom du ikke har bestilt lenke for opplasting kan du se bort fra denne eposten.
<br>
<br>

Trinnvis beskrivelse av hvordan du laster opp et arkiv:
<br>
<ul>
    <li>Siste versjon av program for å laste opp arkivuttrekk finnes her: <a href=https://uploader.digitalisering.arkivverket.no>https://uploader.digitalisering.arkivverket.no</a></li>
    <li>Start applikasjonen</li>
    <li>Trykk på invitasjonslenken i slutten av eposten (starter med dpldr://)</li>
    <li>Velg tar fila som skal lastes opp</li>
</ul>

Invitasjonslenken:
<br>
<a href={upload_url}>{upload_url}</a>
"""
