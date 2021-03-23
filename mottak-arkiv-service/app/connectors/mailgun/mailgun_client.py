from httpx import AsyncClient, BasicAuth
from typing import List
from uuid import UUID

from app.connectors.mailgun.models import InvitasjonUploadUrl, InvitasjonEmail


class MailgunClient(AsyncClient):

    def __init__(self, domain: str, secret: str, tusd_url: str):
        super().__init__()
        self.url = f'https://api.eu.mailgun.net/v3/{domain}/messages'
        self.secret = secret
        self.domain = domain
        self.tusd_url = tusd_url

    async def send_invitasjon(self, to: List[str],
                              arkivuttrekk_obj_id: UUID,
                              arkivuttrekk_tittel: str,
                              invitasjon_ekstern_id: UUID):
        upload_url = InvitasjonUploadUrl(arkivuttrekk_obj_id, self.tusd_url, invitasjon_ekstern_id).as_base64_url()
        email = InvitasjonEmail(self.domain, to, arkivuttrekk_obj_id, arkivuttrekk_tittel, upload_url)
        auth = BasicAuth('api', self.secret)
        resp = await self.post(self.url, auth=auth, data=email.as_data())
        return resp
