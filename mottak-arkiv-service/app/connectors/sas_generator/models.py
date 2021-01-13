import json

from pydantic.main import BaseModel
from uuid import UUID

ZERO_GENERATION = '0'


class SASTokenRequest:
    def __init__(self, container: UUID, duration_hours: int):
        self.container = f'{str(container)}-{ZERO_GENERATION}'
        self.duration_hours = duration_hours

    def as_json(self) -> str:
        return json.dumps(self.__dict__)


class SASResponse(BaseModel):
    """DTO for the response sas object"""
    storage_account: str
    container: str
    sas_token: str
