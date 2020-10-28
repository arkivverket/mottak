import json
import base64
from uuid import UUID
from typing import List


class InvitasjonMelding:
    __url_prefix = 'dpldr://'

    def __init__(self, arkivuttrekk_obj_id: UUID, upload_url: str, invitasjon_uuid: UUID, upload_type: str = 'tar'):
        self.reference = str(arkivuttrekk_obj_id)
        self.upload_url = upload_url
        self.upload_type = upload_type
        self.meta = {'invitasjon_uuid': str(invitasjon_uuid)}

    def as_base64_url(self):
        json_str = json.dumps(self.__dict__)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return self.__url_prefix + base64_str


class MailgunEmail:

    __subject = "Invitasjon til opplasting av Arkivuttrekk"

    def __init__(self, mailgun_domain: str, to: List[str], upload_url: str):
        self.__from = f'Mottak Arkivverket <donotreply@{mailgun_domain}>'
        self.__to = to
        self.__text = f'Opplastingslink for arkivuttrekk: {upload_url}'
        self.__html = f'Opplastingslink for arkivuttrekk: <a href={upload_url}>{upload_url}</a>'

    def as_data(self):
        return {'from': self.__from, 'to': self.__to, 'subject': self.__subject, 'text': self.__text,
                'html': self.__html}
