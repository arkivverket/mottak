from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from app.domain.models.Invitasjon import InvitasjonStatus


class Invitasjon(BaseModel):
    """
    Used as the response model for Invitasjon.
    Contains information about sent invitations.
    """
    id: int
    ekstern_id: UUID
    arkivuttrekk_id: int
    status: InvitasjonStatus
    avgiver_epost: str
    opprettet: datetime

    class Config:
        orm_mode = True
