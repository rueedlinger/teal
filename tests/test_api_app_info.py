import pytest
from starlette.testclient import TestClient

from teal import api


@pytest.mark.parametrize(
    "endpoint", ["/app/info", "/app/health", "/app/metrics", "/docs", "/openapi.json"]
)
def test_app_endpoints_are_upp(endpoint):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    response = client.get(url=f"{endpoint}")
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", ["/app/info", "/app/health", "/app/metrics"])
def test_unknown_query_parameter_are_allowed(endpoint):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    response = client.get(url=f"{endpoint}?foo")
    assert response.status_code == 200

    response = client.get(url=f"{endpoint}?foo=bar")
    assert response.status_code == 200
