import xml.etree.ElementTree as ET

import pytest

from app.domain.metadatafil_service import metadatafil_mapper
from app.domain.models.metadatafil import ParsedMetadatafil, Metadatafil
from app.domain.xmlparser import get_parsedmetadatafil, get_all_namespaces, get_title, \
    get_kontaktperson, get_arkivtype, get_storrelse, get_tidsspenn, get_avtalenummer


@pytest.fixture
def t_innhold(testfile):
    return metadatafil_mapper(testfile).innhold


@pytest.fixture
def t_root(t_innhold):
    return ET.fromstring(t_innhold)


@pytest.fixture
def t_root_errors(testfile_with_errors):
    innhold_errors = metadatafil_mapper(testfile_with_errors).innhold
    return ET.fromstring(innhold_errors)


@pytest.fixture
def t_ns():
    return {'mets': 'http://www.loc.gov/METS/'}


@pytest.fixture
def t_metadatfil(testfile) -> Metadatafil:
    metadatafil = metadatafil_mapper(testfile)
    metadatafil.id = 1
    metadatafil.arkivuttrekk_id = 1
    metadatafil.opprettet = '2020-10-10 00:00:00'
    metadatafil.endret = '2020-10-10 00:00:00'
    return metadatafil


def test_get_all_namespaces(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file
    WHEN    calling the method get_namespaces()
    THEN    check that the returned dictionary is correct
    """
    exepected = t_ns
    actual = get_all_namespaces(t_root)
    assert actual == exepected


def test_get_title_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_title()
    THEN    check that the returned string is correct
    """
    expected = "The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234"
    actual = get_title(t_root, t_ns)

    assert actual == expected


def test_get_title_failure(t_root_errors, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file with missing title values
            and a dictionary with the mets namespace
    WHEN    calling the method get_title()
    THEN    check that the returned string is correct
    """
    # expected = "tittel: Fant ikke tag <agent ROLE=ARCHIVIST, TYPE=ORGANIZATION> -- tittel: Fant ikke LABEL"
    expected = "None -- None"
    actual = get_title(t_root_errors, t_ns)

    assert actual == expected


def test_get_kontaktperson(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_kontaktperson()
    THEN    check that the returned string is correct
    """
    execpected = "Lewis Caroll (lewis@caroll.net)"
    actual = get_kontaktperson(t_root, t_ns)

    assert actual == execpected


def test_get_kontaktperson_failure(t_root_errors, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file with missing contact person values
            and a dictionary with the mets namespace
    WHEN    calling the method get_kontaktperson()
    THEN    check that the returned string is correct
    """
    expected = "None (None)"
    actual = get_kontaktperson(t_root_errors, t_ns)

    assert actual == expected


def test_get_arkivtype_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_arkivtype()
    THEN    check that the returned string is correct
    """
    execpected = "Noark 5 - Sakarkiv"
    actual = get_arkivtype(t_root, t_ns)

    assert actual == execpected


def test_get_arkivtype_failure(t_root_errors, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_arkivtype()
    THEN    check that the returned string is None
    """
    execpected = "None"
    actual = get_arkivtype(t_root_errors, t_ns)

    assert actual == execpected


def test_get_storrelse_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_storrelse()
    THEN    check that the returned string is correct
    """
    execpected = "440320"
    actual = get_storrelse(t_root, t_ns)

    assert actual == execpected


def test_get_tidsspenn_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_tidsspenn()
    THEN    check that the returned string is correct
    """
    execpected = "1863-01-01 -- 1864-12-31"
    actual = get_tidsspenn(t_root, t_ns)

    assert actual == execpected


def test_get_avtalenummer_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_avtalenummer()
    THEN    check that the returned string is correct
    """
    execpected = "01/12345"
    actual = get_avtalenummer(t_root, t_ns)

    assert actual == execpected


def test_get_parsedmetadatfil(t_metadatfil):
    """
    GIVEN   a metadatafil where the content is an METS/XML file
    WHEN    calling the method get_parsedmetadatafil()
    THEN    check that the returned ParsedMetadafil object is correct
    """
    expected = ParsedMetadatafil()
    expected.tittel = "The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234"
    expected.endret = "2020-10-10 00:00:00"
    expected.kontaktperson = "Lewis Caroll (lewis@caroll.net)"
    expected.arkivtype = "Noark 5 - Sakarkiv"
    expected.objekt_id = "UUID:df53d1d8-39bf-4fea-a741-58d472664ce2"
    expected.storrelse = "440320"
    expected.tidsspenn = "1863-01-01 -- 1864-12-31"
    expected.avtalenummer = "01/12345"

    actual = get_parsedmetadatafil(t_metadatfil)

    assert vars(actual) == vars(expected)

