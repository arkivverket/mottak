from datetime import datetime

from pydantic import BaseModel

from services.domain.metadatafil import MetadataType


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
