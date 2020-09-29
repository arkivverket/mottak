from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

# TODO Mock database in pytest


def test_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Seems healthy"


def test_get_archive():
    response = client.get("/arkiv/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_archives():
    response = client.get("/arkiver")
    assert response.status_code == status.HTTP_200_OK

