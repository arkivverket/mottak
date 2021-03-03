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
    invitasjon_id: int
    status: ArkivkopiStatus
    is_object: bool
    target_name: str
    storage_account: str
    container: str
    sas_token_start: datetime
    sas_token_slutt: datetime
    opprettet: datetime
    endret: datetime

    def __init__(self,
                 id_=None,
                 invitasjon_id=None,
                 status=None,
                 is_object=None,
                 target_name=None,
                 storage_account=None,
                 container=None,
                 sas_token_start=None,
                 sas_token_slutt=None,
                 opprettet=None,
                 endret=None):
        self.id = id_
        self.invitasjon_id = invitasjon_id
        self.status = status
        self.is_object = is_object
        self.target_name = target_name
        self.storage_account = storage_account
        self.container = container
        self.sas_token_start = sas_token_start
        self.sas_token_slutt = sas_token_slutt
        self.opprettet = opprettet
        self.endret = endret

    def __eq__(self, other):
        if isinstance(other, Arkivkopi):
            return self.id == other.id and \
                   self.invitasjon_id == other.invitasjon_id and \
                   self.status == other.status and \
                   self.is_object == other.is_object and \
                   self.target_name == other.target_name and \
                   self.storage_account == other.storage_account and \
                   self.container == other.container and \
                   self.sas_token_start == other.sas_token_start and \
                   self.sas_token_slutt == other.sas_token_slutt and \
                   self.opprettet == other.opprettet and \
                   self.endret == other.endret
        return False

    @staticmethod
    def create_from(invitasjon_id: int, sas_token: SASResponse, target_name: str, is_object: bool = False) -> Arkivkopi:
        query_string = parse_qs(sas_token.sas_token)
        sas_token_start = convert_string_to_datetime(query_string["st"][0])
        sas_token_slutt = convert_string_to_datetime(query_string["se"][0])

        return Arkivkopi(invitasjon_id=invitasjon_id,
                         status=ArkivkopiStatus.BESTILT,
                         is_object=is_object,
                         target_name=target_name,
                         storage_account=sas_token.storage_account,
                         container=sas_token.container,
                         sas_token_start=sas_token_start,
                         sas_token_slutt=sas_token_slutt)
