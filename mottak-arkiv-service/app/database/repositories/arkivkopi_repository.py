import pytz
from datetime import datetime
from urllib.parse import parse_qs

from sqlalchemy.orm import Session

from app.database.dbo.mottak import Arkivkopi as Arkivkopi_DBO
from app.domain.models.Arkivkopi import ArkivkopiStatus


def convert_to_datetime(datetime_string: str):
    iso_8601 = '%Y-%m-%dT%H:%M:%S%z'
    return datetime.strptime(datetime_string, iso_8601).astimezone(pytz.timezone("Europe/Oslo"))


def create(db: Session, arkivuttrekk_id: int, status: ArkivkopiStatus, storage_account: str, container: str,
           sas_token: str) -> Arkivkopi_DBO:
    query_string = parse_qs(sas_token)
    sas_token_start = convert_to_datetime(query_string["st"][0])
    sas_token_slutt = convert_to_datetime(query_string["se"][0])

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
