from enum import Enum


class InvitasjonStatus(str, Enum):
    SENDT = 'Sendt'
    FEILET = "Feilet"
