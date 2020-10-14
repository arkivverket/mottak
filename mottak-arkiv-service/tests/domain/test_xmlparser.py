import xml.etree.ElementTree as ET

import pytest

from app.domain.metadatafil_service import metadatafil_mapper
from app.domain.models.metadatafil import ParsedMetadatafil, Metadatafil
from app.domain.xmlparser import get_parsedmetadatafil, get_all_namespaces, get_title, \
    get_kontaktperson, get_arkivtype, get_storrelse, get_tidsspenn, get_avtalenummer, format_size


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


@pytest.mark.parametrize("test_input, expected",
                         [(1, "1e-06 MB"), (1000, "0.001 MB"), (10**6, "1.0 MB"),
                          (10**9, "1000.0 MB"), (10**12, "1000000.0 MB")])
def test_format_size_to_MB(test_input, expected):
    """
    GIVEN   a tuple of test_input, expected output
    WHEN    calling the method format_size()
    THEN    check that the format conversion is correct
    """
    actual = format_size(test_input)
    assert actual == expected


@pytest.mark.parametrize("test_input, expected",
                         [("B", "1000000000.0 B"), ("KB", "1000000.0 KB"),
                          ("MB", "1000.0 MB"), ("GB", "1.0 GB"), ("TB", "0.001 TB")])
def test_format_size_fix_value_to_units(test_input, expected):
    """
    GIVEN   a fixed value of 1 000 000 000 bytes and a list of changing conversion units
    WHEN    calling the method format_size()
    THEN    check that the expected conversion is correct
    """
    size = 10**9
    actual = format_size(size, test_input)
    assert actual == expected


def test_get_storrelse_success(t_root, t_ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method get_storrelse()
    THEN    check that the returned string is correct
    """
    execpected = "0.44032 MB"
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
    expected = ParsedMetadatafil(
        tittel="The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234",
        endret="2020-10-10 00:00:00",
        kontaktperson="Lewis Caroll (lewis@caroll.net)",
        arkivtype="Noark 5 - Sakarkiv",
        objekt_id="UUID:df53d1d8-39bf-4fea-a741-58d472664ce2",
        storrelse="0.44032 MB",
        tidsspenn="1863-01-01 -- 1864-12-31",
        avtalenummer="01/12345"
    )

    actual = get_parsedmetadatafil(t_metadatfil)

    assert vars(actual) == vars(expected)

