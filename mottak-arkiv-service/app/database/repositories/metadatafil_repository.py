from sqlalchemy.orm import Session

from app.database.dbo.mottak import Metadatafil as Metadatafil_DBO
from app.domain.models.Metadatafil import Metadatafil


def create(db: Session, metadatfil: Metadatafil) -> Metadatafil_DBO:
    dbo = Metadatafil_DBO(**vars(metadatfil))
    db.add(dbo)
    db.commit()
    return dbo


def get_by_id(db: Session, id_: int) -> Metadatafil_DBO:
    return db.query(Metadatafil_DBO).get(id_)
