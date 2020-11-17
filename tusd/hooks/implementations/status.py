from enum import Enum


class OverforingspakkeStatus(str, Enum):
    STARTET = 'Startet'
    OK = 'Ok'
    AVBRUTT = 'Avbrutt'
    FEILET = 'Feilet'
