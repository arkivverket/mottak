from __future__ import annotations

import json
import logging
from typing import Optional
from uuid import UUID

from app.connectors.sas_generator.models import SASResponse
from app.domain.models.Arkivkopi import ArkivkopiStatus


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are transferred by the the queue ARCHIVE_DOWNLOAD_REQUEST_SENDER.
    """

    def __init__(self,
                 arkivkopi_id: int,
                 storage_account: str,
                 container: str,
                 sas_token: str):
        self.arkivkopi_id = arkivkopi_id
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequest):
            return self.arkivkopi_id == other.arkivkopi_id and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token == other.sas_token
        return False

    @staticmethod
    def from_id_and_token(arkivkopi_id: int, sas_token: SASResponse):
        return ArkivkopiRequest(arkivkopi_id=arkivkopi_id,
                                storage_account=sas_token["storage_account"],
                                container=sas_token["container"],
                                sas_token=sas_token["sas_token"])

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)


class ArkivkopiStatusResponse:
    def __init__(self, arkivkopi_id: int, status: ArkivkopiStatus):
        self.arkivkopi_id = arkivkopi_id
        self.status = status

    def __eq__(self, other):
        if isinstance(other, ArkivkopiStatusResponse):
            return self.arkivkopi_id == other.arkivkopi_id and \
                   self.status == other.status
        return False

    @staticmethod
    def from_string(json_string: str) -> Optional[ArkivkopiStatusResponse]:
        try:
            json_message = json.loads(json_string)
            return ArkivkopiStatusResponse(**json_message)
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f'Failed to parse message {json_string}', e)
            return None
