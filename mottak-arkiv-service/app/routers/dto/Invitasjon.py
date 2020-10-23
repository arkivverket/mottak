from datetime import datetime
from pydantic import BaseModel

from app.domain.models.Invitasjon import InvitasjonStatus


class Invitasjon(BaseModel):
    """
    Used as the response model for all metadatafiles.
    Contains the METS file which is used as a basis for the archive.
    """
    id: int
    arkivuttrekk_id: int
    status: InvitasjonStatus
    opprettet: datetime

    class Config:
        orm_mode = True
