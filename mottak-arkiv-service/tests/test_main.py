import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from sqlalchemy.orm import Session

client = TestClient(app)


class MockDbQuery:
    @staticmethod
    def get(_id):
        return None

    @staticmethod
    def order_by(*args, **kwargs):
        return MockDbQuery()

    @staticmethod
    def offset(*args, **kwargs):
        return MockDbQuery()

    @staticmethod
    def limit(*args, **kwargs):
        return MockDbQuery()

    @staticmethod
    def all(*args, **kwargs):
        return []


@pytest.fixture()
def mock_db_env(monkeypatch):
    monkeypatch.setenv("DB_DRIVER", "postgresql")
    monkeypatch.setenv("DB_USER", "tester")
    monkeypatch.setenv("DB_PASSWORD", "")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "postgres")
    def mock_response(*args, **kwargs):
        return MockDbQuery()
    monkeypatch.setattr(Session, 'query', mock_response)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Seems healthy"


def test_upload_metadatafil():
    file_path = Path.cwd() / 'testdata' / 'metadatafil1.xml'
    with open(file_path, 'rb') as f:
        response = client.post("metadatafil", files={"file": ("metadatafile.xml", f, "text/xml")})
    assert response.status_code == status.HTTP_201_CREATED


def test_get_archive(mock_db_env):
    response = client.get("/arkiv/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_archives(mock_db_env):
    response = client.get("/arkiver")
    assert response.status_code == status.HTTP_200_OK
