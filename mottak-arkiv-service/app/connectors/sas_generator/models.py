import json

from pydantic.main import BaseModel
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class SASTokenRequest:
    def __init__(self, container: UUID, duration: int):
        self.container = container
        self.duration = duration

    def as_json(self) -> str:
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)


class SASResponse(BaseModel):
    """DTO for the response sas object"""
    storage_account: str
    container: str
    sas_token: str
