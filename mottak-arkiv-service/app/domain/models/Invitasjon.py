from datetime import datetime
from enum import Enum
from uuid import UUID


class InvitasjonStatus(str, Enum):
    SENDT = 'Sendt'
    FEILET = "Feilet"


class Invitasjon:
    def __init__(self,
                 id_: int,
                 ekstern_id: UUID,
                 arkivuttrekk_id: int,
                 avgiver_epost: str,
                 status: InvitasjonStatus,
                 opprettet: datetime):
        self.id = id_
        self.ekstern_id = ekstern_id
        self.arkivuttrekk_id = arkivuttrekk_id
        self.avgiver_epost = avgiver_epost
        self.status = status
        self.opprettet = opprettet

    def __eq__(self, other):
        if isinstance(other, Invitasjon):
            return self.id == other.id and \
                   self.ekstern_id == other.ekstern_id and \
                   self.arkivuttrekk_id == other.arkivuttrekk_id and \
                   self.avgiver_epost == other.avgiver_epost and \
                   self.status == other.status and \
                   self.opprettet == other.opprettet
        return False
