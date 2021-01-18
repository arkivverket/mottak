from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivkopi as Arkivkopi_DBO
from app.domain.models.Arkivkopi import Arkivkopi


def create(db: Session, arkivkopi: Arkivkopi) -> Arkivkopi_DBO:
    dbo = Arkivkopi_DBO(**vars(arkivkopi))
    db.add(dbo)
    db.commit()
    return dbo
