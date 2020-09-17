from __future__ import annotations
import json
from uuid import UUID
from enum import Enum
from datetime import datetime


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class TransferStatus(Enum):
    RECEIVED = 1
    TRANSFERING = 2
    FINISHED = 3
    FAILED = 4


class ArkivuttrekkTransferInfo:
    def __init__(self, obj_id: UUID, blob_sas_url: str):
        self.obj_id = obj_id
        self.blob_sas_url = blob_sas_url

    @staticmethod
    def from_string(json_string: str) -> ArkivuttrekkTransferInfo:
        json_message = json.loads(json_string)
        return ArkivuttrekkTransferInfo(UUID(json_message['obj_id']), json_message['blob_sas_url'])

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)


class ArkivuttrekkTransferStatus:
    def __init__(self, obj_id: UUID, status: TransferStatus):
        self.obj_id = obj_id
        self.status = status
        self.statusCreatedTime = datetime.now()

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)
