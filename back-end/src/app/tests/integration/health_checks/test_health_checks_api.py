import json
from flask.testing import FlaskClient


def test_health_check_returns_ok_status(client: FlaskClient):
    res = client.get("/health_checks")
    assert res.status_code == 200
    assert res.json == {"status": "OK"}
