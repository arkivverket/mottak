from __future__ import annotations

import json
import logging
from enum import Enum
from typing import Optional
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class ArkivkopiStatus(str, Enum):
    BESTILT = 'Bestilt'
    STARTET = 'Startet'
    OK = 'OK'
    AVBRUTT = 'Avbrutt'
    FEILET = 'Feilet'

    @staticmethod
    def get_status(status_str: str) -> ArkivkopiStatus:
        members = [member for member in ArkivkopiStatus.__members__.values() if member.value == status_str]
        if members:
            return members.pop()


class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are retrieved from the queue ARCHIVE_DOWNLOAD_REQUEST_RECEICER.
    """

    def __init__(self,
                 arkivkopi_id: int,
                 arkivuttrekk_id: UUID,
                 status: ArkivkopiStatus,
                 storage_account: str,
                 container: str,
                 sas_token: str):
        self.arkivkopi_id = arkivkopi_id
        self.arkivuttrekk_id = UUID(str(arkivuttrekk_id))
        self.status = ArkivkopiStatus.get_status(status)
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token

    @staticmethod
    def from_string(json_string: str) -> Optional[ArkivkopiRequest]:
        try:
            json_message = json.loads(json_string)
            return ArkivkopiRequest(**json_message)
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f'Failed to parse message {json_string}', e)
            return None

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)


class ArkivkopiStatusResponse:
    def __init__(self, arkivuttrekk_id: UUID, status: ArkivkopiStatus):
        self.arkivuttrekk_id = arkivuttrekk_id
        self.status = status

    def as_json_str(self) -> str:
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)
