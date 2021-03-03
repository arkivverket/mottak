import logging
from datetime import datetime

from app.connectors.sas_generator.models import SASResponse
from app.domain.models.Arkivkopi import ArkivkopiStatus, Arkivkopi

logging.disable(logging.CRITICAL)


def test_arkivkopi_create_from():
    """
    GIVEN   an invitasjon_id, SASResponse (token) and a target_name
    WHEN    calling the method create_from() in Arkivkopi
    THEN    control that the returned Arkivkopi is correct
    """
    expected = Arkivkopi(invitasjon_id=1,
                         status=ArkivkopiStatus.BESTILT,
                         is_object=False,
                         target_name="target_name_test",
                         storage_account="storage_account_test",
                         container="container_test",
                         sas_token_start=datetime.fromisoformat("2021-02-23T15:22:11+01:00"),
                         sas_token_slutt=datetime.fromisoformat("2021-02-23T16:37:11+01:00"))
    sas_token = SASResponse(
        storage_account="storage_account_test",
        container="container_test",
        sas_token="st=2021-02-23T14%3A22%3A11Z&se=2021-02-23T15%3A37%3A11Z&sp=rl&sv=2020-02-10&sr=c&sig=someSignature")
    actual = Arkivkopi.create_from(invitasjon_id=1, sas_token=sas_token, target_name="target_name_test")
    assert actual == expected
