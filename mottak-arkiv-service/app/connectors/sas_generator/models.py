from __future__ import annotations

import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SASTokenRequest:
    def __init__(self, container_id: str, duration_hours: int):
        self.container = container_id
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
            logger.error(f"Failed to create SASResponse from json", e)
            return None
