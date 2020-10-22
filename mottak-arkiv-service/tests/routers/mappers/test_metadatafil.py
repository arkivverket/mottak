import pytest

from app.domain.models.Metadatafil import Metadatafil, MetadataType
from app.routers.mappers.metadafil import _get_file_content, metadatafil_mapper, _content_type2metadata_type


def test__content_type2metadata_type__success():
    """
    GIVEN   the string 'text/xml' as content_type
    WHEN    calling the method _content_type2metadata_type
    THEN    check that return value is MetadataType.XML_METS
    """
    expected = MetadataType.XML_METS
    actual = _content_type2metadata_type('text/xml')
    assert actual == expected


def test__content_type2metadata_type__failure():
    """
    GIVEN   the string 'text' as content_type
    WHEN    calling the method _content_type2metadata_type
    THEN    check that a ValueError Exception has been raised
    """
    with pytest.raises(ValueError):
        _content_type2metadata_type('text')


def test__get_file_content(testfile, testfile_content):
    """
    GIVEN   a file with testdata where the content is an METS/XML file
    WHEN    calling the method _get_file_content
    THEN    check that the returned string is correct
    """
    expected = testfile_content
    actual = _get_file_content(testfile)
    assert actual == expected


def test_metadatafil_mapper(testfile, testfile_content):
    """
    GIVEN   a file with testdata where the content is an METS/XML file
    WHEN    calling the method metadatafil_mapper
    THEN    check that the returned Metadatafil object is correct
    """
    expected = Metadatafil(
        filnavn="df53d1d8-39bf-4fea-a741-58d472664ce2.xml",
        type_=MetadataType.XML_METS,
        innhold=testfile_content)
    actual = metadatafil_mapper(testfile)
    assert vars(actual) == vars(expected)
