from enum import Enum


class InvitasjonStatus(str, Enum):
    SENT = 'Sent'
    FEILET = "Feilet"
