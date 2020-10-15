import pytest

from app.domain.models.metadatafil import ParsedMetadatafil
from app.domain.mappers.metadatafil import map_parsed_domain2dto
from app.domain.models.metadatafil import ParsedMetadatafil as Parsed_DTO


@pytest.fixture
def t_parsed_model():
    return ParsedMetadatafil(
        tittel='tittel',
        endret='endret',
        kontaktperson='kontaktperson',
        arkivtype='arkivtype',
        objekt_id='obekt_id',
        storrelse='størrelse',
        tidsspenn='tidsspenn',
        avtalenummer='avtalenummer'
    )


def test_map_parsed_domain2dto(t_parsed_model):
    """
    GIVEN   a domain object of type ParsedMetadafil
    WHEN    calling the method map_parsed_domain2dto
    THEN    check that the returned ParsedMetadatafil DTO object is correct
    """
    expected = Parsed_DTO(
        tittel='tittel',
        endret='endret',
        kontaktperson='kontaktperson',
        arkivtype='arkivtype',
        objekt_id='obekt_id',
        storrelse='størrelse',
        tidsspenn='tidsspenn',
        avtalenummer='avtalenummer'
    )
    actual = map_parsed_domain2dto(t_parsed_model)
    assert vars(actual) == vars(expected)
