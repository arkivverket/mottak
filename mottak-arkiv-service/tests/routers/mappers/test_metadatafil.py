import pytest

from app.domain.models.metadatafil import Metadatafil, MetadataType, ParsedMetadatafil as Parsed_Model
from app.routers.dto.Metadatafil import ParsedMetadatafil as Parsed_DTO
from app.routers.mappers.metadafil import get_file_content, metadatafil_mapper, content_type2metadata_type, \
    map_parsed_domain2dto


@pytest.fixture
def t_content():
    return "<?xml version=\"1.0\" encoding=\"utf-8\"?><mets:mets xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" OBJID=\"UUID:df53d1d8-39bf-4fea-a741-58d472664ce2\" LABEL=\"Wonderland (1862 - 1864) - 1234\" TYPE=\"SIP\" PROFILE=\"http://xml.ra.se/METS/RA_METS_eARD.xml\" xsi:schemaLocation=\"http://www.loc.gov/METS/ http://schema.arkivverket.no/METS/mets.xsd\" xmlns:mets=\"http://www.loc.gov/METS/\"><mets:metsHdr CREATEDATE=\"1865-01-01T00:00:00\"><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"INDIVIDUAL\"><mets:name>Lewis Caroll</mets:name><mets:note>Guilford, Surrey</mets:note><mets:note>14011898</mets:note><mets:note>lewis@caroll.net</mets:note></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"SUBMITTER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"PRODUCER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"IPOWNER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"CREATOR\" TYPE=\"ORGANIZATION\"><mets:name>Arkivverket</mets:name></mets:agent><mets:agent ROLE=\"PRESERVATION\" TYPE=\"ORGANIZATION\"><mets:name>Arkivverket</mets:name></mets:agent><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"OTHER\" OTHERTYPE=\"SOFTWARE\"><mets:name>Wonderland</mets:name><mets:note>1.0</mets:note><mets:note>Noark5</mets:note><mets:note>Ukjent</mets:note></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"PRODUCER\" TYPE=\"OTHER\" OTHERTYPE=\"SOFTWARE\"><mets:name>Through the Looking Glass</mets:name><mets:note>1.1</mets:note><mets:note>Noark5</mets:note><mets:note>v5.0</mets:note></mets:agent><mets:altRecordID TYPE=\"DELIVERYSPECIFICATION\">Noark 5 - Sakarkiv</mets:altRecordID><mets:altRecordID TYPE=\"SUBMISSIONAGREEMENT\">01/12345</mets:altRecordID><mets:altRecordID TYPE=\"STARTDATE\">1863-01-01</mets:altRecordID><mets:altRecordID TYPE=\"ENDDATE\">1864-12-31</mets:altRecordID></mets:metsHdr><mets:fileSec><mets:fileGrp ID=\"fileGroup001\" USE=\"FILES\"><mets:file ID=\"fileId_0\" MIMETYPE=\"application/tar\" SIZE=\"440320\" CREATED=\"2019-10-29T15:54:59.6548471+01:00\" CHECKSUM=\"2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a\" CHECKSUMTYPE=\"SHA-256\" USE=\"Datafile\"><mets:FLocat LOCTYPE=\"URL\" xlink:type=\"simple\" xlink:href=\"file:df53d1d8-39bf-4fea-a741-58d472664ce2.tar\" /></mets:file></mets:fileGrp></mets:fileSec><mets:structMap><mets:div /></mets:structMap></mets:mets>"


@pytest.fixture
def t_parsed_model():
    return Parsed_Model(
        tittel='tittel',
        endret='endret',
        kontaktperson='kontaktperson',
        arkivtype='arkivtype',
        objekt_id='obekt_id',
        storrelse='størrelse',
        tidsspenn='tidsspenn',
        avtalenummer='avtalenummer'
    )


def test_content_type2metadata_type__success():
    """
    GIVEN   the string 'text/xml' as content_type
    WHEN    calling the method content_type2metadata_type
    THEN    check that return value is MetadataType.XML_METS
    """
    expected = MetadataType.XML_METS
    actual = content_type2metadata_type('text/xml')
    assert actual == expected


def test_content_type2metadata_type__failure():
    """
    GIVEN   the string 'text' as content_type
    WHEN    calling the method content_type2metadata_type
    THEN    check that a ValueError Exception has been raised
    """
    with pytest.raises(ValueError):
        content_type2metadata_type('text')


def test_get_file_content(testfile, t_content):
    """
    GIVEN   a file with testdata where the content is an METS/XML file
    WHEN    calling the method get_file_content
    THEN    check that the returned string is correct
    """
    expected = t_content
    actual = get_file_content(testfile)
    assert actual == expected


def test_metadatafil_mapper(testfile, t_content):
    """
    GIVEN   a file with testdata where the content is an METS/XML file
    WHEN    calling the method metadatafil_mapper
    THEN    check that the returned Metadatafil object is correct
    """
    expected = Metadatafil(
        filnavn="df53d1d8-39bf-4fea-a741-58d472664ce2.xml",
        type=MetadataType.XML_METS,
        innhold=t_content)
    actual = metadatafil_mapper(testfile)
    assert vars(actual) == vars(expected)


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
