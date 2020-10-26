import base64
import json
from httpx import AsyncClient, BasicAuth
from typing import List
from uuid import UUID


class MailgunClient(AsyncClient):

    def __init__(self, domain: str, secret: str, tusd_url: str):
        super().__init__()
        self.url = f'https://api.mailgun.net/v3/{domain}/messages'
        self.secret = secret
        self.domain = domain
        self.tusd_url = tusd_url

    def __build_email_data(self, to: List[str], upload_url: str) -> dict:
        return {'from': f'Mottak <donotreply@{self.domain}>',
                'to': to,
                'subject': "Invitasjon til opplasting av Arkivuttrekk",
                'text': upload_url,
                'html': f'<a href={upload_url}>{upload_url}</a>'}

    def __build_upload_url(self, arkivuttrekk_obj_id: UUID, invitasjon_uuid: UUID):
        message = self.__create_message(arkivuttrekk_obj_id, invitasjon_uuid)
        return self.__create_url_from_message(message)

    def __create_message(self, arkivuttrekk_obj_id: UUID, invitasjon_uuid: UUID) -> dict[str: str]:
        return {'reference': str(arkivuttrekk_obj_id),
                'upload_url': self.tusd_url,
                'upload_type': 'tar',
                'meta': {'invitasjon_uuid': str(invitasjon_uuid)}}

    @staticmethod
    def __create_url_from_message(message_dict: dict[str, str]) -> str:
        json_str = json.dumps(message_dict)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return f'dpldr://{base64_str}'

    async def send_invitasjon(self, to: List[str], arkivuttrekk_obj_id: UUID, invitasjon_uuid: UUID):
        upload_url = self.__build_upload_url(arkivuttrekk_obj_id, invitasjon_uuid)
        auth = BasicAuth('api', self.secret)
        data = self.__build_email_data(to, upload_url)
        resp = await self.post(self.url, auth=auth, data=data)
        return resp
