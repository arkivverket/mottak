import logging

from httpx import AsyncClient, HTTPError
from uuid import UUID

from app.connectors.sas_generator.models import SASResponse, SASTokenRequest


class SASGeneratorClient():
    def __init__(self, sas_url: str):
        self.url = f"{sas_url}/generate_sas"

    async def request_sas(self, container: UUID, duration: int = 24) -> SASResponse:
        async with AsyncClient() as client:
            request = SASTokenRequest(container, duration)

            try:
                resp = await client.post(self.url, data=request.as_json())
            except HTTPError as err:
                logging.error(f"Error while requesting {err.request.url!r}.")
                return False

            if resp.status_code == 412:
                logging.error(f"Fant ikke container med id={container}")
                return False

            if resp.status_code != 200:
                logging.error(f"Det skjedde en feil under genereringen av sas_token for container med id={container}")
                return False

            return resp.json()
