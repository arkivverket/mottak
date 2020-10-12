""" DTO objects for the SAS generator service """
# pylint: disable=no-name-in-module, too-few-public-methods
from typing import Optional
from pydantic.main import BaseModel


class SASRequest(BaseModel):
    """ DTO for the generate_sas endpoint."""
    container: str
    duration_hours: Optional[int] = 1
