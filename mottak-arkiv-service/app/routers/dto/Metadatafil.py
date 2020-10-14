from datetime import datetime

from pydantic import BaseModel

from app.domain.models.metadatafil import MetadataType


class Metadatafil(BaseModel):
    """
    Used as the response model for all metadatafiles.
    Contains the METS file which is used as a basis for the archive.
    """
    id: int
    filnavn: str
    type: MetadataType
    innhold: str
    opprettet: datetime
    endret: datetime

    class Config:
        orm_mode = True


class ParsedMetadatafil(BaseModel):
    """
    Used as the response model for the parsed content of a Metadatafil
    which contains information used for uploading an archive.
    """
    tittel: str
    endret: str
    kontaktperson: str
    arkivtype: str
    objekt_id: str
    storrelse: str
    tidsspenn: str
    avtalenummer: str
