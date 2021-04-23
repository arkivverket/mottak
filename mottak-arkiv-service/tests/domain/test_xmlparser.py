import xml.etree.ElementTree as ET
from datetime import datetime, date
from uuid import UUID

import pytest

from app.routers.services.metadatafil_service import metadatafil_mapper
from app.domain.models.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkStatus, ArkivuttrekkType
from app.domain.models.Metadata import Metadata
from app.domain.models.Metadatafil import Metadatafil
from app.domain.xmlparser import create_metadata_from_parsed_metadatafil, _get_all_namespaces, _get_title, \
    _get_arkivtype, _get_storrelse, _get_avtalenummer, _get_objekt_id, \
    _str_2_arkivuttrekk_type, _get_checksum, _get_avgiver_navn, _get_avgiver_epost, _get_arkiv_startdato, \
    _get_arkiv_sluttdato, _convert_2_megabytes


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


def test__get_all_namespaces(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file
    WHEN    calling the method _get_namespaces()
    THEN    check that the returned dictionary is correct
    """
    exepected = _ns
    actual = _get_all_namespaces(_root)
    assert actual == exepected


def test__get_objekt_id(_root):
    """
    GIVEN   a XML root Element of an METS/XML file
    WHEN    calling the method _get_objekt_id()
    THEN    check that the returned UUID is correct
    """
    expected = UUID("df53d1d8-39bf-4fea-a741-58d472664ce2")
    actual = _get_objekt_id(_root)
    assert actual == expected


@pytest.mark.parametrize("_input, expected",
                         [("Noark 5 - Sakarkiv", ArkivuttrekkType.NOARK5),
                          ("Noark 3 - Sakarkiv", ArkivuttrekkType.NOARK3),
                          ("Fagsystem", ArkivuttrekkType.FAGSYSTEM),
                          ("SIARD-arkivuttrekk fra sak- arkivløsningen ePhorte fra Utdanningsdirektoratet 2004-2017.",
                           ArkivuttrekkType.SIARD),
                          ("Feilaktig verdi som inneholder tallet 5", None)])
def test__str_2_arkivuttrekk_type(_input, expected):
    """
    GIVEN   a tuple of _input, expected output
    WHEN    calling the method _str_2_arkivuttrekk_type()
    THEN    check that the conversion to Enum ArkivuttrekkType is correct
    """
    actual = _str_2_arkivuttrekk_type(_input)
    assert actual == expected


def test_get_arkivtype_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkivtype()
    THEN    check that the returned string is correct
    """
    execpected = "Noark5"
    actual = _get_arkivtype(_root, _ns)
    assert actual == execpected


def test_get_arkivtype_failure(_root_errors, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkivtype()
    THEN    check that the returned string is None
    """
    execpected = None
    actual = _get_arkivtype(_root_errors, _ns)
    assert actual == execpected


def test__get_title_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_title()
    THEN    check that the returned string is correct
    """
    expected = "The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234"
    actual = _get_title(_root, _ns)
    assert actual == expected


def test__get_title_failure(_root_errors, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file with missing title values
            and a dictionary with the mets namespace
    WHEN    calling the method _get_title()
    THEN    check that the returned string is correct
    """
    expected = ""
    actual = _get_title(_root_errors, _ns)
    assert actual == expected


def test__get_checksum(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_checksum()
    THEN    check that the returned string contains the checksum
    """
    expected = '2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a'
    actual = _get_checksum(_root, _ns)
    assert actual == expected


def test__get_avgiver_navn(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_avgiver_navn()
    THEN    check that the returned string is correct
    """
    expected = "Lewis Caroll"
    actual = _get_avgiver_navn(_root, _ns)
    assert actual == expected


def test__get_avgiver_epost(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_avgiver_epost()
    THEN    check that the returned string is correct
    """
    expected = "lewis@caroll.net"
    actual = _get_avgiver_epost(_root, _ns)
    assert actual == expected


def test__get_arkiv_startdato(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkiv_startdato()
    THEN    check that the returned date is correct
    """
    expected = date.fromisoformat("1863-01-01")
    actual = _get_arkiv_startdato(_root, _ns)
    assert actual == expected


def test__get_arkiv_sluttdato(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_arkiv_sluttdato()
    THEN    check that the returned date is correct
    """
    expected = date.fromisoformat("1864-12-31")
    actual = _get_arkiv_sluttdato(_root, _ns)
    assert actual == expected


@pytest.mark.parametrize("_input, expected",
                         [(1, 1e-06), (1000, 0.001), (10 ** 6, 1.0),
                          (10 ** 9, 1000.0), (10 ** 12, 1000000.0)])
def test__convert_2_megabytes(_input, expected):
    """
    GIVEN   a tuple of input, expected output
    WHEN    calling the method _convert_2_megabytes()
    THEN    check that the format conversion is correct
    """
    actual = _convert_2_megabytes(_input)
    assert actual == expected


def test_get_storrelse_success(_root, _ns):
    """
    GIVEN   a XML root Element of an METS/XML file and a dictionary with the mets namespace
    WHEN    calling the method _get_storrelse()
    THEN    check that the returned float is correct
    """
    execpected = 0.44032
    actual = _get_storrelse(_root, _ns)
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


def test_create_metadata_from_parsed_metadatafil(_innhold):
    """
    GIVEN   the content(XML) of a METS/XML file
    WHEN    calling the method create_metadata_from_parsed_metadatafil()
    THEN    check that the returned Arkivuttrekk domain object is correct
    """
    expected = Metadata(
        obj_id=UUID("df53d1d8-39bf-4fea-a741-58d472664ce2"),
        status=ArkivuttrekkStatus.OPPRETTET,
        arkivutrekk_type=ArkivuttrekkType.NOARK5,
        tittel="The Lewis Caroll Society -- Wonderland (1862 - 1864) - 1234",
        sjekksum_sha256="2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a",
        avgiver_navn="Lewis Caroll",
        avgiver_epost="lewis@caroll.net",
        metadatafil_id=1,
        arkiv_startdato=date.fromisoformat("1863-01-01"),
        arkiv_sluttdato=date.fromisoformat("1864-12-31"),
        storrelse=0.44032,
        avtalenummer="01/12345"
    )
    metadatafil_id = 1
    actual = create_metadata_from_parsed_metadatafil(metadatafil_id, _innhold)
    assert vars(actual) == vars(expected)

