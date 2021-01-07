import json
import logging

from typing import Optional
from uuid import UUID

from app.connectors.azure_servicebus.utils import UUIDEncoder

class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are retrieved from the queue ARCHIVE_DOWNLOAD_REQUEST_RECEICER.
    """

    def __init__(self,
                 arkivkopi_id: int,
                 arkivuttrekk_id: UUID,
                 storage_account: str,
                 container: str,
                 sas_token: str):
        self.arkivkopi_id = arkivkopi_id
        self.arkivuttrekk_id = UUID(str(arkivuttrekk_id))
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token

    def __eq__(self, other):
        if isinstance(other, ArkivkopiRequest):
            return self.arkivkopi_id == other.arkivkopi_id and \
                   self.arkivuttrekk_id == other.arkivuttrekk_id and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token == other.sas_token
        return False

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)
