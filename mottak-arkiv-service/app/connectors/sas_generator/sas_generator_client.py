from httpx import AsyncClient
from uuid import UUID

from app.connectors.sas_generator.models import SASTokenRequest

class SASGeneratorClient(AsyncClient):
    def __init__(self, sas_url: str,):
        super().__init__()
        self.url = sas_url

    async def request_sas(self, container: UUID, duration: int = 24):
        request = SASTokenRequest(container, duration)
        resp = await self.post(self.url, data=request.as_data())
        return resp.json()
