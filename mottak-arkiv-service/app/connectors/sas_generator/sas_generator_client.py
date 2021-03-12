import logging
from typing import Optional

from httpx import AsyncClient, HTTPError

from app.connectors.sas_generator.models import SASResponse, SASTokenRequest

logger = logging.getLogger(__name__)


class SASGeneratorClient:
    def __init__(self, sas_generator_host: str):
        self.url = f"http://{sas_generator_host}/generate_sas"

    async def request_sas(self, container_id: str, duration_hours: int = 24) -> Optional[SASResponse]:
        async with AsyncClient() as client:
            request = SASTokenRequest(container_id, duration_hours)

            try:
                resp = await client.post(self.url, data=request.as_json())
            except HTTPError as err:
                logger.error(f"Error while requesting {err.request.url!r}.")
                return None

            if resp.status_code == 412:
                logger.error(f"Could not find container with id={container_id}")
                return None

            if resp.status_code != 200:
                msg = f"Something went wrong during the generation of sas_token for container with id={container_id}"
                logger.error(msg)
                return None

            return SASResponse.from_json(resp.json())
