from __future__ import annotations
import json
from uuid import UUID
from enum import Enum
import logging
from datetime import datetime
from typing import Optional


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class ArkivkopiStatus(Enum):
    BESTILT = 'Bestilt'
    STARTET = 'Startet'
    OK = 'OK'
    AVBRUTT = 'Avbrutt'
    FEILET = 'Feilet'


class ArkivkopiRequest:
    def __init__(self, obj_id: UUID, container_sas_url: str):
        self.obj_id = obj_id
        self.container_sas_url = container_sas_url  # TODO legg til variabel sas_token container og storage_account, transfer-req_id


    @staticmethod
    def from_string(json_string: str) -> Optional[ArkivkopiRequest]:
        try:
            json_message = json.loads(json_string)
            json_message['obj_id'] = UUID(json_message['obj_id'])
            return ArkivkopiRequest(**json_message)
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f'Failed to parse message {json_string}', e)
            return None

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)


class ArkivkopiStatusResponse:
    def __init__(self, obj_id: UUID, status: ArkivkopiStatus):
        self.obj_id = obj_id
        self.status = status
        self.statusCreatedTime = datetime.now()  # TODO Gir denne mening?

    def as_json_str(self) -> str:
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)
