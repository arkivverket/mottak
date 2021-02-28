from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Optional

from app.database.dbo.mottak import Overforingspakke as Overforingspakke_DBO


def get_by_arkivuttrekk_id_newest(db: Session, arkivuttrekk_id: int) -> Optional[Overforingspakke_DBO]:
    return db.query(Overforingspakke_DBO)\
        .filter(Overforingspakke_DBO.arkivuttrekk_id == arkivuttrekk_id)\
        .order_by(desc(Overforingspakke_DBO.endret))\
        .first()
