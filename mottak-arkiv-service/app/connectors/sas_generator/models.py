from __future__ import annotations

import json
import logging
from typing import Optional
from uuid import UUID

ZERO_GENERATION = '0'


class SASTokenRequest:
    def __init__(self, container: UUID, duration_hours: int):
        self.container = f'{str(container)}-{ZERO_GENERATION}'
        self.duration_hours = duration_hours

    def as_json(self) -> str:
        return json.dumps(self.__dict__)


class SASResponse:
    """DTO for the response sas object"""

    def __init__(self, storage_account, container, sas_token):
        self.storage_account = storage_account
        self.container = container
        self.sas_token = sas_token

    @staticmethod
    def from_json(json_message: dict) -> Optional[SASResponse]:
        try:
            return SASResponse(**json_message)
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f"Failed to create SASResponse from json", e)
            return None
