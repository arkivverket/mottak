from __future__ import annotations

import json
import logging
from typing import Optional
from uuid import UUID

from app.domain.models.Arkivkopi import ArkivkopiStatus, ArkivkopiRequestParameters

logger = logging.getLogger(__name__)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class ArkivkopiRequestBlobInfo:
    """
    Optional object included in ArkivkopiRequest if the request is to download a single object from a
    Azure Blob Storage container.
    """
    def __init__(self,
                 source_name: str,
                 target_name: str):
        self.source_name = source_name
        self.target_name = target_name

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequestBlobInfo):
            return self.source_name == other.source_name and \
                   self.target_name == other.target_name


class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are transferred by the the queue ARCHIVE_DOWNLOAD_REQUEST_SENDER.
    """
    def __init__(self,
                 arkivkopi_id: int,
                 storage_account: str,
                 container: str,
                 sas_token: str,
                 blob_info: Optional[ArkivkopiRequestBlobInfo] = None):
        self.arkivkopi_id = arkivkopi_id
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token
        self.blob_info = blob_info

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequest):
            return self.arkivkopi_id == other.arkivkopi_id and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token == other.sas_token and \
                   self.blob_info == other.blob_info
        return False

    @staticmethod
    def from_parameters(parameters: ArkivkopiRequestParameters) -> ArkivkopiRequest:
        sas_token = parameters.sas_token
        blob_info = None
        if parameters.source_name and parameters.target_name:
            blob_info = ArkivkopiRequestBlobInfo(source_name=parameters.source_name,
                                                 target_name=parameters.target_name)
        return ArkivkopiRequest(arkivkopi_id=parameters.arkivkopi_id,
                                storage_account=sas_token.storage_account,
                                container=sas_token.container,
                                sas_token=sas_token.sas_token,
                                blob_info=blob_info)

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=lambda o: o.__dict__)


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
            logger.error(f'Failed to parse message {json_string}', e)
            return None
