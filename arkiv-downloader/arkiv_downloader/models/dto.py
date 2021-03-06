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
    FEILET = 'Feilet'

    @staticmethod
    def get_status(status_str: str) -> ArkivkopiStatus:
        members = [member for member in ArkivkopiStatus.__members__.values() if member.value == status_str]
        if members:
            return members.pop()


class ArkivkopiRequestBlobInfo:
    """
    Optional object included in ArkivkopiRequest if the request is to download a single object from a
    Azure Blob Storage container.
    """

    def __init__(self, source_name: str, target_name: str):
        self.source_name = source_name
        self.target_name = target_name

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequestBlobInfo):
            return self.source_name == other.source_name and \
                   self.target_name == other.target_name


class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are retrieved from the queue ARCHIVE_DOWNLOAD_REQUEST_RECEICER.
    """

    def __init__(self,
                 arkivkopi_id: int,
                 storage_account: str,
                 container: str,
                 sas_token: str,
                 blob_info: Optional[dict] = None):
        self.arkivkopi_id = arkivkopi_id
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token
        self.blob_info = ArkivkopiRequestBlobInfo(**blob_info) if blob_info else None

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequest):
            return self.arkivkopi_id == other.arkivkopi_id and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token == other.sas_token and \
                   self.blob_info == other.blob_info
        return False

    @staticmethod
    def from_string(json_string: str) -> Optional[ArkivkopiRequest]:
        try:
            json_message = json.loads(json_string)
            return ArkivkopiRequest(**json_message)
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f'Failed to parse message {json_string}', e)
            return None

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=lambda o: o.__dict__)

    def as_safe_json_str(self):
        as_dict = self.__dict__.copy()
        as_dict["sas_token"] = "<secret>"
        return json.dumps(as_dict, cls=UUIDEncoder, default=lambda o: o.__dict__)


class ArkivkopiStatusResponse:
    def __init__(self, arkivkopi_id: int, status: ArkivkopiStatus):
        self.arkivkopi_id = arkivkopi_id
        self.status = status

    def as_json_str(self) -> str:
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=lambda o: o.__dict__)
