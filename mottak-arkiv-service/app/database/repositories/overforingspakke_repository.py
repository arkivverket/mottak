from typing import Optional

from sqlalchemy.orm import Session

from app.database.dbo.mottak import Overforingspakke as Overforingspakke_DBO


def get_by_invitasjon_id(db: Session, invitasjon_id: int) -> Optional[Overforingspakke_DBO]:
    return db.query(Overforingspakke_DBO).filter(Overforingspakke_DBO.invitasjon_id == invitasjon_id).first()
