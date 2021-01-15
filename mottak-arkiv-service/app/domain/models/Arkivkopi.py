from __future__ import annotations
from datetime import datetime

import json
from enum import Enum
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Arkivkopi:
    id: int
    arkivuttrekk_id: int
    status: ArkivkopiStatus
    storage_account: str
    container: str
    sas_token_start: datetime
    sas_token_slutt: datetime
    opprettet: datetime
    endret: datetime

    def __init__(self,
                 id_=None,
                 arkivuttrekk_id=None,
                 status=None,
                 storage_account=None,
                 container=None,
                 sas_token_start=None,
                 sas_token_slutt=None,
                 opprettet=None,
                 endret=None):
        self.id = id_
        self.arkivuttrekk_id = arkivuttrekk_id
        self.status = status
        self.storage_account = storage_account
        self.container = container
        self.sas_token_start = sas_token_start
        self.sas_token_slutt = sas_token_slutt
        self.opprettet = opprettet
        self.endret = endret


class ArkivkopiRequest:
    """
    The information needed to make a copy of an archive from cloud to on-prem.
    These objects are retrieved from the queue ARCHIVE_DOWNLOAD_REQUEST_RECEICER.
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

    def as_json_str(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder, default=str)


class ArkivkopiStatus(str, Enum):
    BESTILT = 'Bestilt'
    STARTET = 'Startet'
    OK = 'OK'
    FEILET = 'Feilet'
