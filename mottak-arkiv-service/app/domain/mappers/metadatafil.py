from app.domain.models.metadatafil import ParsedMetadatafil
from app.routers.dto.Metadatafil import ParsedMetadatafil as ParsedMetadatafil_DTO


def map_parsed_domain2dto(domain: ParsedMetadatafil) -> ParsedMetadatafil_DTO:
    """
    Method that converts a domain object of type ParsedMetadatfil into a DTO of type ParsedMetadatafil.
    """
    dto = ParsedMetadatafil_DTO(
        tittel=domain.tittel,
        endret=domain.endret,
        kontaktperson=domain.kontaktperson,
        arkivtype=domain.arkivtype,
        objekt_id=domain.objekt_id,
        storrelse=domain.storrelse,
        tidsspenn=domain.tidsspenn,
        avtalenummer=domain.avtalenummer)
    return dto
