from enum import Enum


class InvitasjonStatus(str, Enum):
    BESTILT = 'Bestilt'
    SENT = 'Sent'
    FEILET = "Feilet"
