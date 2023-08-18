"""
This file (test_home_bp.py) contains the functional tests for the `home` blueprint.
"""
import json


def test_home_page(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert json.loads(response.data) == {
        "status": "running",
    }


def test_home_config_page(test_client):
    response = test_client.get("/config")
    response_data = json.loads(response.data)

    assert response.status_code == 200
    assert "environment" in response_data and response_data["environment"] == "testing"
    assert "debug" in response_data and response_data["debug"] is True
    assert "clusters" in response_data and response_data["clusters"] is None
    assert "loki" in response_data and response_data["loki"] is None
