from typing import Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class MetadataType(str, Enum):
    XML_METS = 'xml/mets'


def get_MetadataType(content_type):
    if 'xml' in content_type:
        return MetadataType.XML_METS
    else:
        raise ValueError(f"Content type {content_type} is not a valid type")


class BaseMetadatafil(BaseModel):
    """This is the minimum version of Metadata"""
    filnavn: str = None
    type: MetadataType = None
    innhold: str = None

    def __init__(self, filename, content_type, xml_string, **data: Any):
        super().__init__(**data)
        self.filnavn = filename
        self.type = get_MetadataType(content_type)
        self.innhold = xml_string


class Metadatafil(BaseMetadatafil):
    """The metadata file which contains the METS file which is used as a basis for the
    archive. If we move away from METS we should change the ENUM field to support other file types."""
    id: int
    arkivuttrekk_id: int = None
    opprettet: datetime

    class Config:
        orm_mode = True
