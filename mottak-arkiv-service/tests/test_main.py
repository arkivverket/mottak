from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

# TODO Mock database in pytest
def test_get_archives():
    response = client.get("/arkiver")
    assert response.status_code == status.HTTP_200_OK

