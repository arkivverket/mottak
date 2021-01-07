from httpx import AsyncClient
from uuid import UUID

from app.connectors.sas_generator.models import SASTokenRequest

class SASGeneratorClient():
    def __init__(self, sas_url: str):
        self.url = sas_url

    async def request_sas(self, container: UUID, duration: int = 24):
        async with AsyncClient() as client:
            request = SASTokenRequest(container, duration)
            return await client.post(self.url, data=request.as_data())
