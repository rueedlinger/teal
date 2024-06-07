from starlette.testclient import TestClient

from teal import api


def test_health():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get(url="/app/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_openapi_json():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get(url="/openapi.json")
    assert response.status_code == 200


def test_openapi_docs():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get(url="/docs")
    assert response.status_code == 200


def test_metrics():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get(url="/app/metrics")
    assert response.status_code == 200


def test_info():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get(url="/app/info")
    assert response.status_code == 200
