from datetime import datetime
from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivkopi as Arkivkopi_DBO
from app.domain.models.Arkivkopi import ArkivkopiStatus


def create(db: Session, arkivuttrekk_id: int, status: ArkivkopiStatus, storage_account: str, container: str,
           sas_token_start: datetime, sas_token_slutt: datetime) -> Arkivkopi_DBO:
    dbo = Arkivkopi_DBO(arkivuttrekk_id=arkivuttrekk_id,
                        status=status,
                        storage_account=storage_account,
                        container=container,
                        sas_token_start=sas_token_start,
                        sas_token_slutt=sas_token_slutt,
                        )

    db.add(dbo)
    db.commit()
    return dbo
