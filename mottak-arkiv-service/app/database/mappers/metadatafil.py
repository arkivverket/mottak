from app.domain.models.Metadatafil import Metadatafil
from app.database.dbo.mottak import Metadatafil as Metadatafil_DBO


def map_dbo2model(dbo: Metadatafil_DBO) -> Metadatafil:
    return Metadatafil(
        id_=dbo.id,
        filnavn=dbo.filnavn,
        type_=dbo.type,
        innhold=dbo.innhold,
        opprettet=dbo.opprettet,
        endret=dbo.endret
    )
