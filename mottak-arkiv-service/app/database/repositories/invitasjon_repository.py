from uuid import UUID

from sqlalchemy.orm import Session

from app.database.dbo.mottak import Invitasjon as Invitasjon_DBO
from app.domain.models.Invitasjon import InvitasjonStatus


def create(db: Session, arkivuttrekk_id: int, avgiver_epost: str, status: InvitasjonStatus,
           invitasjon_ekstern_id: UUID) -> Invitasjon_DBO:
    dbo = Invitasjon_DBO(arkivuttrekk_id=arkivuttrekk_id, status=status, ekstern_id=invitasjon_ekstern_id,
                         avgiver_epost=avgiver_epost)
    db.add(dbo)
    db.commit()
    return dbo
