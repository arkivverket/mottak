import base64
import json
from httpx import AsyncClient, BasicAuth
from typing import List
from uuid import UUID, uuid4


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

    def __build_upload_url(self, upload_id: UUID, tusd_url: str, invitation_id: int):
        json_dict = {'reference': str(upload_id),
                     'upload_url': tusd_url,
                     'upload_type': 'tar',
                     'meta': {'invitation_id': invitation_id}}
        json_str = json.dumps(json_dict)
        json_bytes = json_str.encode('utf-8')
        base64_str = str(base64.b64encode(json_bytes), 'utf-8')
        return f'dpldr//{base64_str}'

    async def send_invitaion(self, to: List[str], invitation_id: int):
        upload_url = self.__build_upload_url(uuid4(), self.tusd_url, invitation_id)
        auth = BasicAuth('api', self.secret)
        data = self.__build_email_data(to, upload_url)
        print(data)
        resp = await self.post(self.url, auth=auth, data=data)
        return resp
