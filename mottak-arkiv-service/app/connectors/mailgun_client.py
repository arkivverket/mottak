from httpx import AsyncClient, BasicAuth


class MailgunClient(AsyncClient):

    def __init__(self, domain: str, secret: str):
        super().__init__()
        self.url = f'https://api.mailgun.net/v3/{domain}/messages'
        self.secret = secret
        self.domain = domain

    def __build_email_data(self) -> dict:
        return {'from': f'Mottak <donotreply@{self.domain}>',
                'to': ['kriwal@arkivverket.no'],
                'subject': "Testing mailgun",
                'text': 'Some more testing of mailgun'}

    async def send_invitaion(self):
        auth = BasicAuth('api', self.secret)
        resp = await self.post(self.url, auth=auth, data=self.__build_email_data())
        return resp
