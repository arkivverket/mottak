from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MetadataType(str, Enum):
    """
    If we move away from METS we should change the ENUM field to support other file types.
    """
    XML_METS = 'xml/mets'


class Metadatafil(BaseModel):
    """
    Used as the response model for all metadatafiles.
    Contains the METS file which is used as a basis for the archive.
    """
    id: int
    arkivuttrekk_id: int = None
    filnavn: str
    type: MetadataType
    innhold: str
    opprettet: datetime

    class Config:
        orm_mode = True
