import pytest
from fastapi import UploadFile

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
