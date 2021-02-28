import logging
from datetime import datetime

from app.connectors.sas_generator.models import SASResponse
from app.domain.models.Arkivkopi import ArkivkopiStatus, Arkivkopi

logging.disable(logging.CRITICAL)


def test_arkivkopi_from_id_and_token():
    """
    GIVEN   an arkivuttrekk_id and a SASResponse (token)
    WHEN    calling the method from_id_and_token() in Arkivkopi
    THEN    control that the returned Arkivkopi is correct
    """
    expected = Arkivkopi(arkivuttrekk_id=1,
                         status=ArkivkopiStatus.BESTILT,
                         storage_account="storage_account_test",
                         container="container_test",
                         sas_token_start=datetime.fromisoformat("2021-02-23T15:22:11+01:00"),
                         sas_token_slutt=datetime.fromisoformat("2021-02-23T16:37:11+01:00"))
    sas_token = SASResponse(
        storage_account="storage_account_test",
        container="container_test",
        sas_token="st=2021-02-23T14%3A22%3A11Z&se=2021-02-23T15%3A37%3A11Z&sp=rl&sv=2020-02-10&sr=c&sig=someSignature")
    actual = Arkivkopi.from_id_and_token(arkivuttrekk_id=1, sas_token=sas_token)
    assert actual == expected
