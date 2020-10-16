from datetime import datetime

import pytest
from fastapi import UploadFile

from app.domain.models.Metadatafil import Metadatafil, MetadataType
from app.utils import get_project_root


@pytest.fixture
def testfile():
    print("conftest.testfile")
    file_path = get_project_root() / 'tests' / 'testdata' / 'metadatafil1.xml'
    with open(file_path, 'rb') as f:
        uploadfile = UploadFile(filename='df53d1d8-39bf-4fea-a741-58d472664ce2.xml', content_type='text/xml', file=f)
        yield uploadfile
        print("unyield testfile")


@pytest.fixture
def testfile_with_errors():
    print("conftest.testfile_with_errors")
    file_path = get_project_root() / 'tests' / 'testdata' / 'metadatafil1_errors.xml'
    with open(file_path, 'rb') as fe:
        uploadfile = UploadFile(filename='df53d1d8-39bf-4fea-a741-58d472664ce2.xml', content_type='text/xml', file=fe)
        yield uploadfile
        print("unyield testfile_with_errors")


@pytest.fixture
def testfile_content() -> str:
    return "<?xml version=\"1.0\" encoding=\"utf-8\"?><mets:mets xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" OBJID=\"UUID:df53d1d8-39bf-4fea-a741-58d472664ce2\" LABEL=\"Wonderland (1862 - 1864) - 1234\" TYPE=\"SIP\" PROFILE=\"http://xml.ra.se/METS/RA_METS_eARD.xml\" xsi:schemaLocation=\"http://www.loc.gov/METS/ http://schema.arkivverket.no/METS/mets.xsd\" xmlns:mets=\"http://www.loc.gov/METS/\"><mets:metsHdr CREATEDATE=\"1865-01-01T00:00:00\"><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"INDIVIDUAL\"><mets:name>Lewis Caroll</mets:name><mets:note>Guilford, Surrey</mets:note><mets:note>14011898</mets:note><mets:note>lewis@caroll.net</mets:note></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"SUBMITTER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"PRODUCER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"IPOWNER\" TYPE=\"ORGANIZATION\"><mets:name>The Lewis Caroll Society</mets:name></mets:agent><mets:agent ROLE=\"CREATOR\" TYPE=\"ORGANIZATION\"><mets:name>Arkivverket</mets:name></mets:agent><mets:agent ROLE=\"PRESERVATION\" TYPE=\"ORGANIZATION\"><mets:name>Arkivverket</mets:name></mets:agent><mets:agent ROLE=\"ARCHIVIST\" TYPE=\"OTHER\" OTHERTYPE=\"SOFTWARE\"><mets:name>Wonderland</mets:name><mets:note>1.0</mets:note><mets:note>Noark5</mets:note><mets:note>Ukjent</mets:note></mets:agent><mets:agent ROLE=\"OTHER\" OTHERROLE=\"PRODUCER\" TYPE=\"OTHER\" OTHERTYPE=\"SOFTWARE\"><mets:name>Through the Looking Glass</mets:name><mets:note>1.1</mets:note><mets:note>Noark5</mets:note><mets:note>v5.0</mets:note></mets:agent><mets:altRecordID TYPE=\"DELIVERYSPECIFICATION\">Noark 5 - Sakarkiv</mets:altRecordID><mets:altRecordID TYPE=\"SUBMISSIONAGREEMENT\">01/12345</mets:altRecordID><mets:altRecordID TYPE=\"STARTDATE\">1863-01-01</mets:altRecordID><mets:altRecordID TYPE=\"ENDDATE\">1864-12-31</mets:altRecordID></mets:metsHdr><mets:fileSec><mets:fileGrp ID=\"fileGroup001\" USE=\"FILES\"><mets:file ID=\"fileId_0\" MIMETYPE=\"application/tar\" SIZE=\"440320\" CREATED=\"2019-10-29T15:54:59.6548471+01:00\" CHECKSUM=\"2afeec307b0573339b3292e27e7971b5b040a5d7e8f7432339cae2fcd0eb936a\" CHECKSUMTYPE=\"SHA-256\" USE=\"Datafile\"><mets:FLocat LOCTYPE=\"URL\" xlink:type=\"simple\" xlink:href=\"file:df53d1d8-39bf-4fea-a741-58d472664ce2.tar\" /></mets:file></mets:fileGrp></mets:fileSec><mets:structMap><mets:div /></mets:structMap></mets:mets>"


@pytest.fixture
def testfile_metadatfil(testfile_content) -> Metadatafil:
    return Metadatafil(
        id_=1,
        filnavn="df53d1d8-39bf-4fea-a741-58d472664ce2.xml",
        type_=MetadataType.XML_METS,
        innhold=testfile_content,
        opprettet=datetime.fromisoformat('2020-02-02 00:00:00')
    )
