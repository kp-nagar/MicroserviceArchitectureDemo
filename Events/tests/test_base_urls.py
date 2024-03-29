from app import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_index_url():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "events service is up."