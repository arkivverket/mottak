import xml.etree.ElementTree as ET
from datetime import datetime

import pytest

from app.domain.metadatafil_service import metadatafil_mapper
from app.domain.models.metadatafil import ParsedMetadatafil, Metadatafil
from app.domain.xmlparser import get_parsedmetadatafil, _get_all_namespaces, _get_title, \
    _get_kontaktperson, _get_arkivtype, _get_storrelse, _get_tidsspenn, _get_avtalenummer, _format_size


@pytest.fixture
def _innhold(testfile):
    return metadatafil_mapper(testfile).innhold


@pytest.fixture
def _root(_innhold):
    return ET.fromstring(_innhold)


@pytest.fixture
def _root_errors(testfile_with_errors):
    innhold_errors = metadatafil_mapper(testfile_with_errors).innhold
    return ET.fromstring(innhold_errors)


@pytest.fixture
def _ns():
    return {'mets': 'http://www.loc.gov/METS/'}


@pytest.fixture
def _metadatfil(testfile) -> Metadatafil:
    metadatafil = metadatafil_mapper(testfile)
    metadatafil.id = 1
    metadatafil.opprettet = datetime.fromisoformat('2020-10-10 00:00:00')
    metadatafil.endret = datetime.fromisoformat('2020-10-10 00:00:00')
    return metadatafil


def test_get_all_namespaces(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file
    WHEN    calling the method _get_namespaces()
    THEN    check that the returned dictionary is correct
    """
    exepected = _ns
    actual = _get_all_namespaces(_root)
    assert actual == exepected


def test_get_title_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_title()
    THEN    check that the returned string is correct
    """
    expected = "The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234"
    actual = _get_title(_root, _ns)
    assert actual == expected


def test_get_title_failure(_root_errors, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file with missing title values
            and a dictionary with the mets namespace
    WHEN    calling the method _get_title()
    THEN    check that the returned string is correct
    """
    expected = "None -- None"
    actual = _get_title(_root_errors, _ns)
    assert actual == expected


def test_get_kontaktperson(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_kontaktperson()
    THEN    check that the returned string is correct
    """
    execpected = "Lewis Caroll (lewis@caroll.net)"
    actual = _get_kontaktperson(_root, _ns)
    assert actual == execpected


def test_get_kontaktperson_failure(_root_errors, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file with missing contact person values
            and a dictionary with the mets namespace
    WHEN    calling the method _get_kontaktperson()
    THEN    check that the returned string is correct
    """
    expected = "None (None)"
    actual = _get_kontaktperson(_root_errors, _ns)
    assert actual == expected


def test_get_arkivtype_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkivtype()
    THEN    check that the returned string is correct
    """
    execpected = "Noark 5 - Sakarkiv"
    actual = _get_arkivtype(_root, _ns)
    assert actual == execpected


def test_get_arkivtype_failure(_root_errors, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkivtype()
    THEN    check that the returned string is None
    """
    execpected = "None"
    actual = _get_arkivtype(_root_errors, _ns)
    assert actual == execpected


@pytest.mark.parametrize("test_input, expected",
                         [(1, "1e-06 MB"), (1000, "0.001 MB"), (10 ** 6, "1.0 MB"),
                          (10 ** 9, "1000.0 MB"), (10 ** 12, "1000000.0 MB")])
def test_format_size_to_MB(test_input, expected):
    """
    GIVEN   a tuple of test_input, expected output
    WHEN    calling the method _format_size()
    THEN    check that the format conversion is correct
    """
    actual = _format_size(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input, expected",
                         [("B", "1000000000.0 B"), ("KB", "1000000.0 KB"),
                          ("MB", "1000.0 MB"), ("GB", "1.0 GB"), ("TB", "0.001 TB")])
def test_format_size_fix_value_to_units(test_input, expected):
    """
    GIVEN   a fixed value of 1 000 000 000 bytes and a list of changing conversion units
    WHEN    calling the method _format_size()
    THEN    check that the expected conversion is correct
    """
    size = 10 ** 9
    actual = _format_size(size, test_input)
    assert actual == expected


def test_get_storrelse_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_storrelse()
    THEN    check that the returned string is correct
    """
    execpected = "0.44032 MB"
    actual = _get_storrelse(_root, _ns)
    assert actual == execpected


def test_get_tidsspenn_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_tidsspenn()
    THEN    check that the returned string is correct
    """
    execpected = "1863-01-01 -- 1864-12-31"
    actual = _get_tidsspenn(_root, _ns)
    assert actual == execpected


def test_get_avtalenummer_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_avtalenummer()
    THEN    check that the returned string is correct
    """
    execpected = "01/12345"
    actual = _get_avtalenummer(_root, _ns)
    assert actual == execpected


def test_get_parsedmetadatfil(_metadatfil):
    """
    GIVEN   a metadatafil where the content is an METS/XML file
    WHEN    calling the method _get_parsedmetadatafil()
    THEN    check that the returned ParsedMetadafil object is correct
    """
    expected = ParsedMetadatafil(
        tittel="The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234",
        endret=datetime.fromisoformat("2020-10-10 00:00:00"),
        kontaktperson="Lewis Caroll (lewis@caroll.net)",
        arkivtype="Noark 5 - Sakarkiv",
        objekt_id="UUID:df53d1d8-39bf-4fea-a741-58d472664ce2",
        storrelse="0.44032 MB",
        tidsspenn="1863-01-01 -- 1864-12-31",
        avtalenummer="01/12345"
    )
    actual = get_parsedmetadatafil(_metadatfil)
    assert vars(actual) == vars(expected)
