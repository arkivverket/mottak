from __future__ import annotations
from datetime import datetime

import json
import logging
from enum import Enum
from typing import Optional
from uuid import UUID
from urllib.parse import parse_qs

from app.connectors.sas_generator.models import SASResponse
from app.utils import convert_string_to_datetime


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

    def from_id_and_token(arkivuttrekk_id: int, sas_token: SASResponse) -> Arkivkopi:
        query_string = parse_qs(sas_token["sas_token"])
        sas_token_start = convert_string_to_datetime(query_string["st"][0])
        sas_token_slutt = convert_string_to_datetime(query_string["se"][0])

        return Arkivkopi(arkivuttrekk_id=arkivuttrekk_id,
                         status=ArkivkopiStatus.BESTILT,
                         storage_account=sas_token["storage_account"],
                         container=sas_token["container"],
                         sas_token_start=sas_token_start,
                         sas_token_slutt=sas_token_slutt)


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

    def from_id_and_token(arkivkopi_id: int, sas_token: SASResponse) -> ArkivkopiRequest:
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
