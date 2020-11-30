from enum import Enum


class OverforingspakkeStatus(str, Enum):
    STARTET = 'Startet'
    OK = 'OK'
    AVBRUTT = 'Avbrutt'
    FEILET = 'Feilet'
