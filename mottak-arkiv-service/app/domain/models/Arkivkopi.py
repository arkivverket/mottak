from __future__ import annotations
from datetime import datetime

from enum import Enum
from urllib.parse import parse_qs

from app.connectors.sas_generator.models import SASResponse
from app.utils import convert_string_to_datetime


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

    def __eq__(self, other):
        if isinstance(other, Arkivkopi):
            return self.id == other.id and \
                   self.arkivuttrekk_id == other.arkivuttrekk_id and \
                   self.status == other.status and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token_start == other.sas_token_start and \
                   self.sas_token_slutt == other.sas_token_slutt and \
                   self.opprettet == other.opprettet and \
                   self.endret == other.endret
        return False

    @staticmethod
    def from_id_and_token(arkivuttrekk_id: int, sas_token: SASResponse) -> Arkivkopi:
        query_string = parse_qs(sas_token.sas_token)
        sas_token_start = convert_string_to_datetime(query_string["st"][0])
        sas_token_slutt = convert_string_to_datetime(query_string["se"][0])

        return Arkivkopi(arkivuttrekk_id=arkivuttrekk_id,
                         status=ArkivkopiStatus.BESTILT,
                         storage_account=sas_token.storage_account,
                         container=sas_token.container,
                         sas_token_start=sas_token_start,
                         sas_token_slutt=sas_token_slutt)
