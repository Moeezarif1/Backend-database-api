from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_credentials():
    response = client.post("/credentials", json={
        "dbname": "testdb",
        "user": "testuser",
        "password": "testpassword",
        "host": "testhost",
        "port": 5432
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Credentials added successfully"


def test_get_schema_not_found():
    response = client.get("/9999")  # Assuming 9999 is a non-existent database ID
    assert response.status_code == 404
