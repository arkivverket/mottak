from pathlib import Path
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

# TODO Mock database in pytest


def test_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Seems healthy"


def test_upload_metadatafil():
    file_path = Path.cwd() / 'testdata' / 'metadatafil1.xml'
    with open(file_path, 'rb') as f:
        response = client.post("metadatafil", files={"file": ("metadatafile.xml", f, "text/xml")})
    assert response.status_code == status.HTTP_201_CREATED


def test_get_archive():
    response = client.get("/arkiv/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_archives():
    response = client.get("/arkiver")
    assert response.status_code == status.HTTP_200_OK
