import base64
import json
from httpx import AsyncClient, BasicAuth
from typing import List
from uuid import UUID

from app.connectors.InvitasjonMelding import InvitasjonMelding


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

    async def send_invitasjon(self, to: List[str], arkivuttrekk_obj_id: UUID, invitasjon_uuid: UUID):
        message = InvitasjonMelding(arkivuttrekk_obj_id, self.tusd_url, invitasjon_uuid)
        auth = BasicAuth('api', self.secret)
        data = self.__build_email_data(to, message.as_base64_url())
        resp = await self.post(self.url, auth=auth, data=data)
        return resp
