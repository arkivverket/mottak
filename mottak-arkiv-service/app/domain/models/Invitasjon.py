from enum import Enum
from uuid import UUID


class InvitasjonStatus(str, Enum):
    SENDT = 'Sendt'
    FEILET = "Feilet"


class Invitasjon:
    def __init__(self,
                 id_: int,
                 ekstern_id: UUID):
        self.id = id_
        self.ekstern_id = ekstern_id

    def __eq__(self, other):
        if isinstance(other, Invitasjon):
            return self.id == other.id and \
                   self.ekstern_id == other.ekstern_id
        return False
