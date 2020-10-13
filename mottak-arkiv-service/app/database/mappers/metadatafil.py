
from app.domain.models.metadatafil import Metadatafil as Metadatafil_domain
from app.database.dbo.mottak import Metadatafil as Metadatafil_DBO

def map_dbo2model(dbo: Metadatafil_DBO) -> Metadatafil_domain:
    return Metadatafil_domain(
        id=dbo.id,
        filnavn=dbo.filnavn,
        type=dbo.type,
        innhold=dbo.innhold,
        opprettet=str(dbo.opprettet),
        endret=str(dbo.endret)
    )
