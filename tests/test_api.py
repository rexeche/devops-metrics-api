from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_record_deployment():
    payload = {
        "service_name": "incontext",
        "environment": "production",
        "version": "2.4.1",
        "status": "success"
    }
    response = client.post("/deployments", json=payload)
    assert response.status_code == 200
    assert response.json()["total_records"] >= 1


def test_list_deployments():
    response = client.get("/deployments")
    assert response.status_code == 200
    assert "deployments" in response.json()


def test_get_metrics():
    # Record a deployment first
    client.post("/deployments", json={
        "service_name": "test-service",
        "environment": "dev",
        "version": "1.0.0",
        "status": "success"
    })
    response = client.get("/metrics/test-service")
    assert response.status_code == 200
    assert response.json()["total_deploys"] >= 1