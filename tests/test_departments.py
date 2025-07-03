# tests/test_departments.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    print(response.text) 
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
