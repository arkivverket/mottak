from httpx import AsyncClient, BasicAuth
from typing import List
from uuid import UUID

from app.connectors.mailgun.models import InvitasjonMelding, MailgunEmail


class MailgunClient(AsyncClient):

    def __init__(self, domain: str, secret: str, tusd_url: str):
        super().__init__()
        self.url = f'https://api.mailgun.net/v3/{domain}/messages'
        self.secret = secret
        self.domain = domain
        self.tusd_url = tusd_url

    async def send_invitasjon(self, to: List[str], arkivuttrekk_obj_id: UUID, invitasjon_ekstern_id: UUID):
        message = InvitasjonMelding(arkivuttrekk_obj_id, self.tusd_url, invitasjon_ekstern_id)
        email = MailgunEmail(self.domain, to, message.as_base64_url())
        auth = BasicAuth('api', self.secret)
        resp = await self.post(self.url, auth=auth, data=email.as_data())
        return resp
